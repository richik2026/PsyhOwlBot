from dataclasses import dataclass


@dataclass
class RatingItem:
    name: str
    count: int
    amount: float = 0


def format_sales_rating(items: list[RatingItem], title: str = "🏆 ТОП администраторов по продажам") -> str:
    lines = [title, ""]

    medals = ["🥇", "🥈", "🥉"]
    for index, item in enumerate(items):
        medal = medals[index] if index < len(medals) else f"{index + 1}."
        lines.append(
            f"{medal} {item.name} — {item.count} подписок — {item.amount:,.0f} ₽"
        )

    return "\n".join(lines)


def format_reels_rating(items: list[RatingItem], title: str = "🎬 ТОП Reels") -> str:
    lines = [title, ""]

    medals = ["🥇", "🥈", "🥉"]
    for index, item in enumerate(items):
        medal = medals[index] if index < len(medals) else f"{index + 1}."
        lines.append(f"{medal} {item.name} — {item.count} Reels")

    return "\n".join(lines)
