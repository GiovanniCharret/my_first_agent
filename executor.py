class Executor:
    def execute(self, command):
        if command["action"] == "add":
            a = command["a"]
            b = command["b"]
            return {"result": a + b}
        else:
            raise ValueError("Unknown action")