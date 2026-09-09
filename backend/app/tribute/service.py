from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.sales.models import Sale
from app.users.models import User


async def process_tribute_payment(
    session: AsyncSession,
    user_id: int,
    amount: float,
    payment_id: str,
):
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
        currency="RUB",
    )

    session.add(sale)
    await session.commit()

    return sale
