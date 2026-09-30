class VoicePipeline:
    """Core Sovenok voice processing pipeline.

    Flow:
    audio -> STT -> AI -> TTS
    """

    def __init__(self, stt, ai, tts, memory=None):
        self.stt = stt
        self.ai = ai
        self.tts = tts
        self.memory = memory

    async def process(self, user_id, audio):
        text = await self.stt.transcribe(audio)

        context = []
        if self.memory:
            context = await self.memory.get_context(user_id)

        answer = await self.ai.reply(text, context)

        if self.memory:
            await self.memory.save(user_id, text, answer)

        return await self.tts.generate(answer)
