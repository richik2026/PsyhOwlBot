from app.reels.service import add_reels


async def request_reels_count_message():
    return "Укажите количество рилсов которое вы выложили за сегодня"


async def save_reels_count(session, admin_id: int, count: int):
    return await add_reels(
        session=session,
        admin_id=admin_id,
        number_of_reels=count,
    )
