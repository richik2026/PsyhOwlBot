from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.sales.models import Sale
from app.subscriptions.service import activate_subscription
from app.users.models import User

SUCCESS_MESSAGE = (
    "Рад тебя видеть, теперь тебе доступно целых 60 часов разговоров со мной! "
    "Проведём их с пользой, жду тебя у себя в кабинете🦉"
)


async def process_tribute_payment(
    session: AsyncSession,
    user_id: int,
    amount: float,
    payment_id: str,
    currency: str = "RUB",
):
    if not payment_id:
        raise ValueError("Missing Tribute payment id")

    existing = await session.scalar(
        select(Sale).where(Sale.provider_payment_id == payment_id)
    )
    if existing:
        return existing, False

    user = await session.scalar(
        select(User).where(User.telegram_id == user_id)
    )
    if not user:
        raise ValueError("User not found")

    sale = Sale(
        user_id=user.id,
        admin_id=user.referrer_admin_id,
        provider="tribute",
        provider_payment_id=payment_id,
        amount=amount,
        currency=currency,
    )
    session.add(sale)

    await activate_subscription(session, user.id)
    await session.commit()

    return sale, True
