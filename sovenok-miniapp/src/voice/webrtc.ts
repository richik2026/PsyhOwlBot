export async function connectRealtimeVoice(
  endpoint: string,
  clientSecret: string
): Promise<RTCPeerConnection> {
  const pc = new RTCPeerConnection();

  const stream = await navigator.mediaDevices.getUserMedia({
    audio: true,
  });

  stream.getTracks().forEach((track) => {
    pc.addTrack(track, stream);
  });

  const audio = document.createElement("audio");
  audio.autoplay = true;

  pc.ontrack = (event) => {
    audio.srcObject = event.streams[0];
  };

  const offer = await pc.createOffer();
  await pc.setLocalDescription(offer);

  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${clientSecret}`,
      "Content-Type": "application/sdp",
    },
    body: offer.sdp,
  });

  const answer = await response.text();

  await pc.setRemoteDescription({
    type: "answer",
    sdp: answer,
  });

  return pc;
}
