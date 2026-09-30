class MemoryService:

    def __init__(self, repository=None):
        self.repository = repository


    async def get_context(self, user_id: int):
        if self.repository:
            return await self.repository.get_recent(user_id)

        return []


    async def save_summary(self, user_id: int, summary: str, importance: float = 0.5):
        if self.repository:
            await self.repository.create(
                user_id=user_id,
                summary=summary,
                importance=importance,
            )
