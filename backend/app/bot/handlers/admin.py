from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.admins.dashboard import format_admin_dashboard, get_admin_dashboard
from app.admins.service import appoint_admin, get_admin_by_telegram_id
from app.admins.models import Admin
from app.users.models import User
from app.sales.models import Sale
from app.referrals.service import build_referral_url, get_or_create_admin_referral

router = Router()


def get_place_icon(index: int) -> str:
    if index == 1:
        return "🥇"
    elif index == 2:
        return "🥈"
    elif index == 3:
        return "🥉"
    else:
        return "🐣"


def admin_panel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Добавить рилсы",
                    callback_data="add_reels"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔗 Моя реферальная ссылка",
                    callback_data="my_referral"
                )
            ],
        ]
    )


async def open_admin_panel(session: AsyncSession, telegram_id: int, send):
    admin = await get_admin_by_telegram_id(session, telegram_id)

    if admin is None or not admin.is_active:
        await send("Эта команда доступна только администраторам")
        return

    data = await get_admin_dashboard(session, admin)

    await send(
        format_admin_dashboard(data),
        parse_mode="HTML",
        reply_markup=admin_panel_keyboard()
    )


async def _send_admin_panel(message: Message, session: AsyncSession):
    await open_admin_panel(
        session,
        message.from_user.id,
        message.answer
    )


@router.message(Command("admin_panel"))
async def admin_panel(message: Message, session: AsyncSession):
    await _send_admin_panel(message, session)


@router.message(Command("my_stats"))
async def my_stats(message: Message, session: AsyncSession):
    await _send_admin_panel(message, session)


@router.message(Command("userstop"))
async def userstop(message: Message, session: AsyncSession):

    admin = await get_admin_by_telegram_id(
        session,
        message.from_user.id
    )

    if admin is None or not admin.is_active:
        await message.answer(
            "Эта команда доступна только администраторам"
        )
        return


    admin_user = aliased(User)

    result = await session.execute(
        select(
            Admin.id,
            admin_user.username,
            func.count(User.id).label("users_count")
        )
        .outerjoin(
            User,
            User.referrer_admin_id == Admin.id
        )
        .outerjoin(
            admin_user,
            admin_user.telegram_id == Admin.telegram_id
        )
        .where(
            Admin.is_active.is_(True)
        )
        .group_by(
            Admin.id,
            admin_user.username
        )
        .order_by(
            func.count(User.id).desc()
        )
    )


    rows = result.all()

    lines = [
        "🏆 <b>Топ администраторов по приглашённым пользователям</b>\n\n",
        ""
    ]


    for index, row in enumerate(rows, 1):

        username = (
            f"@{row.username}"
            if row.username
            else f"ID {row.id}"
        )

        medal = get_place_icon(index)

        lines.append(
            f"{medal} <b>{index} место</b> — {username}\n"
            f"👥 Пользователей: {row.users_count}\n"
        )


    await message.answer(
        "".join(lines),
        parse_mode="HTML"
    )



@router.message(Command("moneytop"))
async def moneytop(message: Message, session: AsyncSession):

    admin = await get_admin_by_telegram_id(
        session,
        message.from_user.id
    )

    if admin is None or not admin.is_active:
        await message.answer(
            "Эта команда доступна только администраторам"
        )
        return


    admin_user = aliased(User)


    result = await session.execute(
        select(
            Admin.id,
            admin_user.username,
            func.count(Sale.user_id).label("sales_count"),
            func.coalesce(
                func.sum(Sale.amount),
                0
            ).label("money"),
        )
        .outerjoin(
            Sale,
            Sale.admin_id == Admin.id
        )
        .outerjoin(
            admin_user,
            admin_user.telegram_id == Admin.telegram_id
        )
        .where(
            Admin.is_active.is_(True)
        )
        .group_by(
            Admin.id,
            admin_user.username
        )
        .order_by(
            func.sum(Sale.amount).desc()
        )
    )


    rows = result.all()


    lines = [
        "💰 <b>Топ администраторов по продаже подписок</b>\n\n",
        ""
    ]


    for index, row in enumerate(rows, 1):

        username = (
            f"@{row.username}"
            if row.username
            else f"ID {row.id}"
        )

        medal = get_place_icon(index)


        lines.append(
            f"{medal} <b>{index} место</b> — {username}\n"
            f"👥 Покупателей: {row.sales_count}\n"
            f"💳 Сумма: {row.money} ₽"
        )


    await message.answer(
        "".join(lines),
        parse_mode="HTML"
    )



@router.message(Command("admin"))
async def admin_command(message: Message, session: AsyncSession):

    parts = message.text.split()

    if len(parts) != 2:
        await message.answer(
            "Использование:\n/admin USER_ID"
        )
        return


    try:
        target_id = int(parts[1])

    except ValueError:
        await message.answer(
            "USER_ID должен быть числом"
        )
        return


    try:

        admin = await appoint_admin(
            session,
            actor_telegram_id=message.from_user.id,
            target_telegram_id=target_id
        )


        referral = await get_or_create_admin_referral(
            session,
            admin
        )


        bot_username = (
            await message.bot.get_me()
        ).username


        link = build_referral_url(
            bot_username,
            referral.code
        )


        await message.bot.send_message(
            target_id,
            f"🦉 Поздравляю, ты стал частью семьи!\n\n"
            f"🤍 Твоя персональная ссылка:\n{link}"
        )


        await session.commit()


        await message.answer(
            "Администратор назначен и ссылка отправлена 🦉"
        )


    except PermissionError:
        await message.answer(
            "Недостаточно прав"
        )
