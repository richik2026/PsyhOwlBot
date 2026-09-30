from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class VoiceSession:
    user_id: int
    started_at: datetime = field(default_factory=datetime.utcnow)
    duration_seconds: int = 0
    transcript: list[str] = field(default_factory=list)

    def add_text(self, text: str):
        self.transcript.append(text)

    def finish(self, seconds: int):
        self.duration_seconds = seconds
