from pathlib import Path
from controller import Controller

class FixedOddPlanner:
    def __init__(self):
        self.calls = 0

    def plan(self):
        self.calls += 1
        # 1+2 = 3 (ímpar) -> validator vai bloquear
        return {"action": "add", "a": 1, "b": 2}

def test_controller_retries_and_fails(tmp_path: Path):
    state_file = tmp_path / "state.json"

    planner = FixedOddPlanner()
    controller = Controller(planner=planner, state_file=state_file, start_fresh=True)

    state = controller.run()

    assert planner.calls == 3
    assert state.attempts == 3
    assert state.status == "FAILED"

    # persistiu
    assert state_file.exists()
    content = state_file.read_text(encoding="utf-8")
    assert '"status": "FAILED"' in content