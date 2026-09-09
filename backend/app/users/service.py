from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def get_or_create_user(
    session: AsyncSession,
    *,
    telegram_id: int,
    username: str | None = None,
    first_name: str | None = None,
    referrer_admin_id: int | None = None,
) -> tuple[User, bool]:
    """Create/update a Telegram user while preserving first-touch attribution."""
    user = await get_user_by_telegram_id(session, telegram_id)
    if user is not None:
        user.username = username
        user.first_name = first_name
        await session.flush()
        return user, False

    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        referrer_admin_id=referrer_admin_id,
    )
    session.add(user)
    await session.flush()
    return user, True
