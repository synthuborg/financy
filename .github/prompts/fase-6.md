**Contexto Inicial Obrigatório:** Leia `.github/copilot/instrucoes-gerais/`, `.github/skills/` e `.github/agents/`. Aplique os conceitos de escalabilidade definidos lá.

**Objetivo:** Expandir a arquitetura implementando contas correntes, cartões e metas financeiras. *Esta é a feature surpresa para demonstrar controle automatizado.*

**Tarefas:**
1. Torne o relacionamento entre `Transaction` e `Account` obrigatório e funcional nos formulários e serviços.
2. Refatore os serviços (`services.py`) para exigir a conta/cartão de origem em cada movimentação. Envolva as operações de saldo em blocos `transaction.atomic()` para garantir segurança.
3. Atualize o template do Dashboard para separar e exibir o saldo por conta (ex: Carteira: R$50, Nubank: R$1000). O saldo de cartões deve refletir a fatura atual.
4. Crie o modelo `Goal` (Meta: nome, valor_alvo, valor_atual). Implemente a lógica no `services.py` e exiba uma barra de progresso visual (CSS) no Dashboard calculando a porcentagem de conclusão.

**Ação Final Obrigatória:** Escreva e execute os testes para as novas regras de múltiplas contas e metas. Atualize o `README.md` criando uma seção "Evolução do Sistema" para explicar à banca como a organização inicial da arquitetura permitiu essa expansão rápida com o auxílio da IA.