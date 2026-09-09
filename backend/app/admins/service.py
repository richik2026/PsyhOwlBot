from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.models import Admin
from app.referrals.service import get_or_create_admin_referral

MAIN_ADMIN_TELEGRAM_ID = 8707664475
VALID_ROLES = {"SUPER_ADMIN", "ADMIN", "SUPPORT", "CONTENT"}


async def get_admin_by_telegram_id(session: AsyncSession, telegram_id: int) -> Admin | None:
    result = await session.execute(select(Admin).where(Admin.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def ensure_main_admin(session: AsyncSession) -> Admin:
    admin = await get_admin_by_telegram_id(session, MAIN_ADMIN_TELEGRAM_ID)
    if admin is None:
        admin = Admin(
            telegram_id=MAIN_ADMIN_TELEGRAM_ID,
            role="SUPER_ADMIN",
            is_active=True,
        )
        session.add(admin)
    else:
        admin.role = "SUPER_ADMIN"
        admin.is_active = True

    await session.flush()
    return admin


async def appoint_admin(
    session: AsyncSession,
    *,
    actor_telegram_id: int,
    target_telegram_id: int,
    role: str = "ADMIN",
) -> Admin:
    if actor_telegram_id != MAIN_ADMIN_TELEGRAM_ID:
        raise PermissionError("Only the main admin can appoint administrators")

    normalized_role = role.upper()
    if normalized_role not in VALID_ROLES:
        raise ValueError(f"Unsupported admin role: {role}")

    admin = await get_admin_by_telegram_id(session, target_telegram_id)
    if admin is None:
        admin = Admin(
            telegram_id=target_telegram_id,
            role=normalized_role,
            is_active=True,
        )
        session.add(admin)
    else:
        admin.role = normalized_role
        admin.is_active = True

    await session.flush()
    await get_or_create_admin_referral(session, admin)
    return admin


async def deactivate_admin(
    session: AsyncSession,
    *,
    actor_telegram_id: int,
    target_telegram_id: int,
) -> Admin:
    if actor_telegram_id != MAIN_ADMIN_TELEGRAM_ID:
        raise PermissionError("Only the main admin can deactivate administrators")
    if target_telegram_id == MAIN_ADMIN_TELEGRAM_ID:
        raise ValueError("The main admin cannot be deactivated")

    admin = await get_admin_by_telegram_id(session, target_telegram_id)
    if admin is None:
        raise LookupError("Admin not found")

    admin.is_active = False
    await session.flush()
    return admin
