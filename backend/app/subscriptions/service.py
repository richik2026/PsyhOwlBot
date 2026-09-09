from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.subscriptions.models import Subscription

SUBSCRIPTION_DAYS = 30
TOTAL_SECONDS = 60 * 60 * 60
DAILY_LIMIT_SECONDS = 2 * 60 * 60


async def activate_subscription(session: AsyncSession, user_id: int) -> Subscription:
    result = await session.execute(
        select(Subscription).where(Subscription.user_id == user_id)
    )
    subscription = result.scalar_one_or_none()
    now = datetime.utcnow()

    if subscription is None:
        subscription = Subscription(
            user_id=user_id,
            active_until=now + timedelta(days=SUBSCRIPTION_DAYS),
            total_seconds=TOTAL_SECONDS,
            used_seconds=0,
            daily_limit_seconds=DAILY_LIMIT_SECONDS,
        )
        session.add(subscription)
        return subscription

    base = subscription.active_until if subscription.active_until > now else now
    subscription.active_until = base + timedelta(days=SUBSCRIPTION_DAYS)
    subscription.total_seconds += TOTAL_SECONDS
    subscription.daily_limit_seconds = DAILY_LIMIT_SECONDS
    return subscription


def remaining_seconds(subscription: Subscription) -> int:
    return max(0, subscription.total_seconds - subscription.used_seconds)


def has_active_access(subscription: Subscription | None) -> bool:
    return bool(
        subscription
        and subscription.active_until > datetime.utcnow()
        and remaining_seconds(subscription) > 0
    )
