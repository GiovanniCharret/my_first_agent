import random

class Planner:
    def plan(self):
        return {
            "action": "add",
            "a": random.randint(1, 5),
            "b": random.randint(1, 5),
        }