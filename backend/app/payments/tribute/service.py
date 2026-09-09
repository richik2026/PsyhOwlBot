from datetime import datetime, timedelta


SUCCESS_MESSAGE = (
    "Рад тебя видеть, теперь тебе доступно целых 60 часов разговоров со мной! "
    "Проведём их с пользой, жду тебя у себя в кабинете🦉"
)


async def process_successful_payment(event, session):
    """
    Processing flow:
    1. Validate payment event.
    2. Find user.
    3. Resolve referral admin.
    4. Create sale record.
    5. Activate subscription.
    6. Notify user.

    Database operations are intentionally kept behind this service layer.
    """
    if not event.payment_id:
        raise ValueError("Missing Tribute payment id")

    # TODO: connect to Sales and Subscription repositories
    # TODO: add idempotency check by provider_payment_id
    # TODO: send Telegram notification after successful commit

    return {
        "status": "processed",
        "payment_id": event.payment_id,
        "processed_at": datetime.utcnow(),
    }
