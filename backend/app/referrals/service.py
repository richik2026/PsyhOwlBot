import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admins.models import Admin
from app.referrals.models import ReferralLink


async def get_referral_by_code(session: AsyncSession, code: str) -> ReferralLink | None:
    result = await session.execute(select(ReferralLink).where(ReferralLink.code == code))
    return result.scalar_one_or_none()


async def get_or_create_admin_referral(session: AsyncSession, admin: Admin) -> ReferralLink:
    result = await session.execute(select(ReferralLink).where(ReferralLink.admin_id == admin.id))
    link = result.scalar_one_or_none()
    if link is not None:
        return link

    for _ in range(5):
        code = f"adm_{secrets.token_urlsafe(8)}"
        exists = await get_referral_by_code(session, code)
        if exists is None:
            link = ReferralLink(admin_id=admin.id, code=code)
            session.add(link)
            await session.flush()
            return link

    raise RuntimeError("Unable to generate unique referral code")


async def resolve_referrer_admin_id(session: AsyncSession, start_parameter: str | None) -> int | None:
    if not start_parameter or not start_parameter.startswith("adm_"):
        return None

    link = await get_referral_by_code(session, start_parameter)
    if link is None:
        return None

    admin = await session.get(Admin, link.admin_id)
    if admin is None or not admin.is_active:
        return None

    return admin.id


def build_referral_url(bot_username: str, code: str) -> str:
    username = bot_username.lstrip("@")
    return f"https://t.me/{username}?start={code}"
