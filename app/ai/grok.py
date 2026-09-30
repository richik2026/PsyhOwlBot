import httpx


class GrokClient:
    def __init__(self, api_key: str, model: str = "grok-4"):
        self.api_key = api_key
        self.model = model

    async def reply(self, text: str, memory: list | None = None):
        messages = [
            {
                "role": "system",
                "content": (
                    "Ты Совёнок. Голосовой AI-компаньон. "
                    "Отвечай коротко, тепло и естественно."
                ),
            },
            {
                "role": "user",
                "content": text,
            },
        ]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                },
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]
