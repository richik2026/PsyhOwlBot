def format_sales_rating(items):
    if not items:
        return "🏆 ТОП администраторов по продажам\n\nПока нет продаж"

    lines = ["🏆 ТОП администраторов по продажам", ""]
    medals = ["🥇", "🥈", "🥉"]
    for index, item in enumerate(items, start=1):
        medal = medals[index - 1] if index <= 3 else f"{index}."
        lines.append(f"{medal} {item['name']} — {item['subscriptions']} подписок — {item['amount']} ₽")
    return "\n".join(lines)


def format_reels_rating(items):
    if not items:
        return "🎬 ТОП Reels\n\nПока нет данных"

    lines = ["🎬 ТОП Reels", ""]
    medals = ["🥇", "🥈", "🥉"]
    for index, item in enumerate(items, start=1):
        medal = medals[index - 1] if index <= 3 else f"{index}."
        lines.append(f"{medal} {item['name']} — {item['reels']} Reels")
    return "\n".join(lines)
