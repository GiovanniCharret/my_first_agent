import json
from pathlib import Path

DEFAULT_STATE_FILE = Path("data/state.json")

class AgentState:
    def __init__(self, attempts=0, status="INIT", last_result=None, state_file: Path | None = None):
        self.attempts = attempts
        self.status = status
        self.last_result = last_result
        self._state_file = state_file or DEFAULT_STATE_FILE

    def to_dict(self):
        return {
            "attempts": self.attempts,
            "status": self.status,
            "last_result": self.last_result,
        }

    @classmethod
    def from_dict(cls, data, state_file: Path | None = None):
        return cls(
            attempts=data.get("attempts", 0),
            status=data.get("status", "INIT"),
            last_result=data.get("last_result"),
            state_file=state_file
        )

    def save(self):
        self._state_file.parent.mkdir(exist_ok=True)
        with open(self._state_file, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, state_file: Path | None = None):
        state_file = state_file or DEFAULT_STATE_FILE
        if not state_file.exists():
            return cls(state_file=state_file)

        try:
            with open(state_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return cls(state_file=state_file)
                data = json.loads(content)
            return cls.from_dict(data, state_file=state_file)
        except json.JSONDecodeError:
            return cls(state_file=state_file)