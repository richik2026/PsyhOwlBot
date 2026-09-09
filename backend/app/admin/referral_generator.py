from uuid import uuid4


def generate_admin_referral_code(admin_id: int) -> str:
    """Generate unique referral code for administrator."""
    suffix = uuid4().hex[:6]
    return f"adm_{admin_id}_{suffix}"


def build_referral_link(bot_username: str, code: str) -> str:
    """Build Telegram deep link for admin referral."""
    return f"https://t.me/{bot_username}?start={code}"


WELCOME_ADMIN_MESSAGE = """Добро пожаловать в семью🦉

Твоя персональная ссылка:

{link}

Все пользователи, которые придут по ней и оформят подписку, будут учитываться в твоей статистике 📈"""


def build_admin_welcome_message(link: str) -> str:
    return WELCOME_ADMIN_MESSAGE.format(link=link)
