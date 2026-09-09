from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.models import Admin


SUPER_ADMIN_ID = 8707664475


async def is_super_admin(telegram_id: int) -> bool:
    return telegram_id == SUPER_ADMIN_ID


async def create_admin(
    session: AsyncSession,
    telegram_id: int,
    role: str = "admin",
):
    result = await session.execute(
        select(Admin).where(Admin.telegram_id == telegram_id)
    )
    admin = result.scalar_one_or_none()

    if admin:
        return admin

    admin = Admin(
        telegram_id=telegram_id,
        role=role,
    )

    session.add(admin)
    await session.commit()
    await session.refresh(admin)

    return admin
