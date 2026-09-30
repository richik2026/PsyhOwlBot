from fastapi import WebSocket


async def voice_socket(websocket: WebSocket, pipeline):
    await websocket.accept()

    while True:
        audio = await websocket.receive_bytes()

        response = await pipeline.process(
            user_id=None,
            audio=audio
        )

        await websocket.send_bytes(response)
