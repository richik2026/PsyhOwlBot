from fastapi import WebSocket


async def voice_socket(websocket: WebSocket, realtime_client):
    """
    Voice bridge for OpenAI Realtime.

    The Mini App now uses realtime audio instead of
    uploading recorded audio chunks.
    """

    await websocket.accept()

    session = await realtime_client.create_session()

    await websocket.send_json(
        {
            "type": "realtime_session",
            "session": session,
        }
    )

    while True:
        message = await websocket.receive_text()

        if message == "close":
            break
