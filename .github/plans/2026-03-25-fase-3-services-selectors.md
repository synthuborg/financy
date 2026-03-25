# Plano: Fase 3 — Services e Selectors (finances/)

**Data:** 2026-03-25
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Implementar funções de serviço e consulta no módulo `finances/` (CRUD de Transaction e cálculo de saldo), cobrindo 100% com testes unitários independentes de HTTP, seguindo o padrão Services/Selectors do projeto.

---

## Escopo

### Incluido
- `finances/services.py` — 4 novas funções: `create_transaction`, `update_transaction`, `delete_transaction`, `calculate_balance`
- `finances/selectors.py` — 2 novas funções: `get_all_transactions`, `get_transaction_by_id`
- Testes unitários em `finances/tests.py` para todas as funções acima
- Nenhuma rota HTTP ou view envolvida nesta fase

### Fora de escopo
- Views, URLs, templates ou formulários Django
- Integração com dashboard ou frontend
- Importação de extratos (já existe — `process_bank_statement_import`)
- Testes E2E Playwright (nenhuma interface nova nesta fase)

---

## Referência de Modelos

```
Transaction
  - valor: DecimalField (>= 0.01, validators=[MinValueValidator('0.01')])
  - data: DateField
  - tipo: CharField ['entrada' | 'saida']
  - descricao: CharField(255)
  - categoria: FK → Category (null/blank)
  - conta: FK → Account (null/blank)
  - usuario: FK → User

Category
  - nome, tipo, usuario, keywords

Account
  - nome, tipo, usuario
```

---

## Checklist de Execucao

### Leitura de Skills (pré-requisito)
- [ ] Ler `django-patterns` SKILL para confirmar convenções de services/selectors
- [ ] Ler `testing-workflow` SKILL para confirmar estratégia de testes unitários
- [ ] Ler `code-review` SKILL para checklist de revisão pós-implementação
- [ ] Ler `django-project-standards.instructions.md` para regras de arquitetura

---

### Backend — `finances/services.py`

#### `create_transaction(user, data: dict) -> Transaction`
- [ ] **RED** — Escrever teste: criação com dados válidos retorna instância Transaction
- [ ] **RED** — Escrever teste: `valor=0` ou negativo levanta `ValidationError`
- [ ] **RED** — Escrever teste: `tipo` inválido levanta `ValidationError`
- [ ] **RED** — Escrever teste: `data` ausente levanta `ValidationError`
- [ ] **GREEN** — Implementar `create_transaction` com `full_clean()` antes de salvar
- [ ] Garantir que a função usa `@db_transaction.atomic` ou equivalente
- [ ] Garantir escopo: `usuario=user` fixado na criação

#### `update_transaction(transaction_id, user, data: dict) -> Transaction`
- [ ] **RED** — Escrever teste: atualização bem-sucedida retorna Transaction atualizado
- [ ] **RED** — Escrever teste: ID inexistente ou de outro usuário levanta `Http404`
- [ ] **RED** — Escrever teste: `valor` inválido no update levanta `ValidationError`
- [ ] **GREEN** — Implementar com `get_object_or_404(Transaction, pk=transaction_id, usuario=user)`
- [ ] Garantir que apenas campos presentes em `data` são atualizados (update parcial seguro)

#### `delete_transaction(transaction_id, user) -> None`
- [ ] **RED** — Escrever teste: deleção bem-sucedida remove o objeto do banco
- [ ] **RED** — Escrever teste: ID inexistente ou de outro usuário levanta `Http404`
- [ ] **GREEN** — Implementar com escopo de usuário antes de deletar

#### `calculate_balance(user) -> dict`
- [ ] **RED** — Escrever teste: sem transações retorna `{'total_entradas': 0, 'total_saidas': 0, 'saldo_liquido': 0}`
- [ ] **RED** — Escrever teste: com entradas e saídas retorna valores exatos (usar `Decimal`)
- [ ] **RED** — Escrever teste: saldo negativo possível (saídas > entradas)
- [ ] **GREEN** — Implementar com `aggregate(Sum('valor'))` filtrado por tipo e usuário
- [ ] Garantir que o retorno usa `Decimal('0')` como valor default (não `None`)

---

### Backend — `finances/selectors.py`

#### `get_all_transactions(user) -> QuerySet`
- [ ] **RED** — Escrever teste: retorna apenas transações do usuário autenticado
- [ ] **RED** — Escrever teste: não retorna transações de outro usuário
- [ ] **RED** — Escrever teste: resultado já inclui `select_related('categoria', 'conta')` (inspecionar `query`)
- [ ] **GREEN** — Implementar com `Transaction.objects.filter(usuario=user).select_related('categoria', 'conta')`
- [ ] Garantir ordenação padrão: usa `Meta.ordering = ['-data']` do modelo

#### `get_transaction_by_id(transaction_id, user) -> Transaction`
- [ ] **RED** — Escrever teste: retorna Transaction correta por ID e usuário
- [ ] **RED** — Escrever teste: ID de outro usuário levanta `Http404`
- [ ] **RED** — Escrever teste: ID inexistente levanta `Http404`
- [ ] **GREEN** — Implementar com `get_object_or_404(Transaction, pk=transaction_id, usuario=user)`

---

### Revisão de Código
- [ ] Executar checklist da skill `code-review`: sem dead code, sem imports desnecessários, sem comentários óbvios
- [ ] Validar PEP8 (nomes snake_case, linhas ≤ 88 chars, docstrings curtas)
- [ ] Confirmar que nenhum dado sensível do usuário é logado
- [ ] Verificar ausência de queries N+1 (select_related aplicado nos selectors)

---

### Testes — Execução Final
- [ ] Todos os testes da fase passando: `pytest finances/tests.py -v`
- [ ] Nenhum teste existente quebrado: `pytest --tb=short`
- [ ] Cobertura das novas funções ≥ 90%: `pytest --cov=finances --cov-report=term-missing`

---

### Git
- [ ] Ler `git-workflow` SKILL antes do commit
- [ ] Stage apenas arquivos desta fase: `finances/services.py`, `finances/selectors.py`, `finances/tests.py`
- [ ] Commit com mensagem Conventional Commits:
  ```
  feat(finances): add CRUD services and selectors for Transaction

  - create_transaction, update_transaction, delete_transaction
  - calculate_balance returning totals and net balance
  - get_all_transactions with select_related optimization
  - get_transaction_by_id with user-scoped 404 guard
  - unit tests covering success and failure paths
  ```

---

## Riscos e Premissas

- **Risco:** `Http404` em services pode ser inadequado para contextos não-HTTP (ex: tasks assíncronas). Avaliar se faz sentido levantar `Transaction.DoesNotExist` e deixar a view tratar o 404.
- **Risco:** `full_clean()` não valida `ForeignKey` nulo quando `null=True` — testes devem cobrir criação sem categoria e sem conta explicitamente.
- **Premissa:** `conftest.py` já expõe a fixture `usuario` (confirmado nos testes existentes).
- **Premissa:** O banco de dados de teste usa SQLite em memória (padrão pytest-django).
- **Premissa:** Não há validação de formulário nesta fase — toda validação é no service layer.

---

## Log de Progresso

- 2026-03-25: Plano criado. Escopo definido, modelos mapeados, checklist TDD detalhado elaborado.

---

## Validacao Final
- [ ] Todos os itens do checklist marcados
- [ ] `pytest` passando sem erros
- [ ] Nenhuma regressão em testes existentes
- [ ] Código revisado com skill `code-review`
- [ ] Commit realizado seguindo `git-workflow`
- [ ] Nenhum item bloqueado
