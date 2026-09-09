from typing import Optional

from sqlalchemy import select

from app.users.models import User


async def get_or_create_user(
    session,
    telegram_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    referrer_admin_id: Optional[int] = None,
) -> User:
    """Return existing user or create a new Telegram user.

    Referral attribution is stored only once. The first referrer wins.
    """

    stmt = select(User).where(User.telegram_id == telegram_id)
    user = await session.scalar(stmt)

    if user:
        if user.referrer_admin_id is None and referrer_admin_id:
            user.referrer_admin_id = referrer_admin_id
            await session.commit()
            await session.refresh(user)
        return user

    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        referrer_admin_id=referrer_admin_id,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
