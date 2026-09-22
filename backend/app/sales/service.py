from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.sales.models import Sale
from app.ratings.service import RatingItem


async def create_sale(
    session: AsyncSession,
    user_id: int,
    admin_id: int | None,
    amount: float,
    provider_payment_id: str | None = None,
) -> Sale:
    sale = Sale(
        user_id=user_id,
        admin_id=admin_id,
        amount=amount,
        provider_payment_id=provider_payment_id,
    )
    session.add(sale)
    await session.commit()
    await session.refresh(sale)
    return sale


async def get_sales_rating(
    session: AsyncSession,
    start_date=None,
) -> list[RatingItem]:
    query = (
        select(
            Sale.admin_id,
            func.count(Sale.id),
            func.sum(Sale.amount),
        )
        .where(Sale.admin_id.is_not(None))
        .group_by(Sale.admin_id)
        .order_by(func.count(Sale.id).desc())
    )

    if start_date:
        query = query.where(Sale.created_at >= start_date)

    result = await session.execute(query)

    return [
        RatingItem(
            name=str(admin_id),
            count=count,
            amount=float(amount or 0),
        )
        for admin_id, count, amount in result.all()
    ]
