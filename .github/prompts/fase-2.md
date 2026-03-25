**Contexto Inicial Obrigatório:** Antes de gerar qualquer código, leia e aplique as diretrizes contidas em `.github/copilot/instrucoes-gerais/`, `.github/skills/` e `.github/agents/`.

**Objetivo:** Construir a camada de dados do app `finances` com foco em integridade relacional e escalabilidade para a fase final.

**Tarefas:**
1. Desenvolva os modelos principais no `models.py`: `Category` (nome, tipo) e `Transaction` (valor, data, tipo [receita/despesa], descrição, fk para categoria). Utilize os tipos de campos mais adequados e adicione validações a nível de banco (ex: valor > 0).
2. Para garantir o sucesso da fase extra futura, crie o modelo `Account` (nome, tipo [conta corrente/carteira/cartao_credito]). Relacione `Account` com `Transaction` (use `null=True, blank=True` temporariamente para não travar a entrega base).
3. Registre todos os modelos no `admin.py` com listagens ricas (`list_display`, `search_fields`, `list_filter`).
4. Escreva testes unitários focados na integridade dos modelos e em seus métodos `__str__`.

**Ação Final Obrigatória:** Gere as migrações e execute os testes de banco de dados. Atualize o `README.md` documentando o dicionário de dados gerado, as decisões de modelagem e o comando exato para aplicar as migrações localmente.