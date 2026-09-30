from openai import AsyncOpenAI


client = AsyncOpenAI()


async def transcribe(audio: bytes) -> str:
    result = await client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.webm", audio),
    )

    return result.text
