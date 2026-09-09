from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.referrals.models import ReferralLink


async def get_admin_by_referral_code(
    session: AsyncSession,
    code: str,
):
    result = await session.execute(
        select(ReferralLink).where(ReferralLink.code == code)
    )

    referral = result.scalar_one_or_none()

    if not referral:
        return None

    return referral.admin_id
