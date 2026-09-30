from openai import AsyncOpenAI


client = AsyncOpenAI()


async def synthesize(text: str) -> bytes:
    response = await client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
    )

    return await response.aread()
