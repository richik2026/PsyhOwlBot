export async function createRealtimeSession(userId?: number) {
  const response = await fetch(
    "/api/voice/realtime/session",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId ?? null,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to create realtime session");
  }

  return response.json();
}
