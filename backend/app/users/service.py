from typing import Optional

from sqlalchemy import select

from app.users.models import User


async def get_or_create_user(
    session,
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
) -> User:
    """Return existing user or create a new Telegram user."""

    stmt = select(User).where(User.telegram_id == telegram_id)
    user = await session.scalar(stmt)

    if user:
        return user

    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
