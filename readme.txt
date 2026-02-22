my_first_agent — Engenharia de Agentes (Single Loop + Multiagente)

Descrição
---------
Este projeto implementa uma arquitetura explícita de agente baseada em:

- Controller (state owner)
- Planner
- Executor determinístico
- Validator determinístico
- Política de retry
- Persistência de estado em JSON
- Logs estruturados

Fase 1 — Single Loop
--------------------
Implementa um loop controlado com:

while attempts < max_attempts:
    plan
    execute
    validate

Invariantes:
- Apenas o Controller altera o estado
- Executor é determinístico
- Validator é determinístico
- Planner não valida
- Anti-circularidade aplicada

O estado é persistido em data/state.json.


Fase 2 — Multiagente
--------------------
Evolução para:

- Controller central
- Workers stateless
- Comunicação tipada (Command, Result)
- Circuit breaker simples
- Separação explícita de responsabilidades


Como executar
-------------

1. Criar ambiente virtual:
   python -m venv .venv

2. Ativar no PowerShell:
   .\.venv\Scripts\Activate.ps1

3. Instalar dependências:
   pip install -r requirements.txt

4. Executar agente:
   python main.py

5. Rodar testes:
   pytest


Objetivo educacional
--------------------
Este projeto não usa frameworks de agentes.
Ele demonstra arquitetura explícita, controle de estado,
retry policy, validação determinística e separação estrutural.

É base para evolução futura para:
- Agentes com LLM
- Multiagentes reais
- Persistência de evidências
- Orquestração distribuída