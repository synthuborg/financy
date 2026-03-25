**Contexto Inicial Obrigatório:** Revise os arquivos de contexto em `.github/copilot/instrucoes-gerais/`, `.github/skills/` e `.github/agents/` antes de prosseguir. O foco aqui é isolamento lógico.

**Objetivo:** Implementar as regras de negócio isoladas das views, fortalecendo a Arquitetura Limpa no app `finances`.

**Tarefas:**
1. No arquivo `services.py`, crie funções puramente focadas no negócio para: criar, editar e deletar transações. Faça tratamento de exceções adequado.
2. Crie uma função `calculate_balance` que processe e retorne o total de receitas, total de despesas e o saldo líquido.
3. No arquivo `selectors.py`, crie as funções de busca (ex: `get_all_transactions()`, `get_transaction_by_id()`), otimizando as queries com `select_related` ou `prefetch_related` quando necessário.
4. Escreva testes unitários rigorosos cobrindo os serviços e seletores, atestando que a lógica funciona de forma independente de qualquer requisição HTTP.

**Ação Final Obrigatória:** Execute a bateria de testes unitários. Atualize o `README.md` com a explicação de como o fluxo de dados funciona (View -> Service/Selector -> Model) e registre a conclusão da Fase 3.