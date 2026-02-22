from state import AgentState
from planner import Planner
from executor import Executor
from validator import Validator
from logger import log

MAX_ATTEMPTS = 3


class Controller:
    """
    Controller = state owner.
    - Orquestra o loop: PLAN -> EXECUTE -> VALIDATE.
    - Aplica retry policy (max attempts).
    - Persiste snapshot final em JSON.
    - Pode rodar idempotente (fresh) ou retomar (resume).
    """

    def __init__(
        self,
        planner=None,
        executor=None,
        validator=None,
        *,
        state_file=None,
        mode="fresh",  # "fresh" (idempotente) | "resume" (carrega do arquivo)
    ):
        if mode not in ("fresh", "resume"):
            raise ValueError('mode must be "fresh" or "resume"')

        self.planner = planner or Planner()
        self.executor = executor or Executor()
        self.validator = validator or Validator()

        # Estado: idempotente por padrão ("fresh")
        if mode == "fresh":
            self.state = AgentState(state_file=state_file)
        else:
            self.state = AgentState.load(state_file=state_file)

    def run(self):
        """
        Executa o loop com no máximo MAX_ATTEMPTS tentativas.
        Retorna o estado final para facilitar testes de integração.
        """
        # Invariante: se estiver resuming e já acabou, não roda loop
        if self.state.attempts >= MAX_ATTEMPTS or self.state.status in ("SUCCESS", "FAILED"):
            log("SKIP_RUN", {"reason": "state already terminal", "state": self.state.to_dict()})
            self.state.save()
            log("FINAL_STATE", self.state.to_dict())
            return self.state

        # Loop principal
        while self.state.attempts < MAX_ATTEMPTS:
            self.state.attempts += 1
            log("ATTEMPT", {"attempt": self.state.attempts})

            command = self.planner.plan()
            log("PLAN", command)

            result = self.executor.execute(command)
            log("EXECUTE", result)

            # Guardar último resultado SEMPRE ajuda debug (mesmo se inválido)
            self.state.last_result = result

            valid, message = self.validator.validate(result)
            log("VALIDATE", {"valid": valid, "message": message})

            if valid:
                self.state.status = "SUCCESS"
                break

            self.state.status = "RETRY"

        # Pós-loop
        if self.state.status != "SUCCESS":
            self.state.status = "FAILED"

        self.state.save()
        log("FINAL_STATE", self.state.to_dict())
        return self.state