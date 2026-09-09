# Import all SQLAlchemy models here so Alembic can discover metadata.

from app.users.models import User
from app.admins.models import Admin
from app.referrals.models import ReferralLink
from app.settings.models import Setting
from app.reels.models import AdminReels
from app.sales.models import Sale

__all__ = [
    "User",
    "Admin",
    "ReferralLink",
    "Setting",
    "AdminReels",
    "Sale",
]
