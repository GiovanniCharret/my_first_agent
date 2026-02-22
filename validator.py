class Validator:
    def validate(self, result):
        value = result["result"]
        if value % 2 != 0:
            return False, "Result is not even"
        return True, "Valid"