# Plano: Transações por Conta no Card de Conta Corrente

**Data:** 2026-03-25
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Exibir as últimas 5 transações de cada conta dentro do card na página de Contas Correntes (`financas/conta-corrente/`), mostrando descrição, data, tipo (entrada/saída com cor verde/vermelho) e valor.

---

## Escopo

### Incluído
- Novo selector `get_transactions_by_account(account_id, user, limit=5)` em `finances/selectors.py`
- Modificar `ContaCorrenteListView.get_context_data()` para incluir transações por conta
- Modificar template `finances/conta_corrente_list.html` para exibir transações dentro do card
- Design: lista compacta dentro do card glass, com cores verde/vermelho para entrada/saída

### Fora de escopo
- Paginação de transações dentro do card
- Filtros de transações dentro do card
- Nova rota/URL
- Novo model

---

## Contexto Técnico

| Artefato | Localização | Detalhes |
|---|---|---|
| View | `finances/views.py` L287-306 | `ContaCorrenteListView` — monta `contas_com_saldo` como lista de tuplas `(conta, saldo)` |
| Selector | `finances/selectors.py` L10-25 | `get_account_balance(account_id, user)` — calcula saldo por conta |
| Template | `finances/templates/finances/conta_corrente_list.html` | Grid de cards glass com saldo, nome, tipo, botões editar/excluir |
| Model Transaction | `finances/models.py` L64-97 | Campos: `valor`, `data`, `tipo`, `descricao`, `categoria` (FK), `conta` (FK), `usuario` (FK) |
| Testes | `finances/tests.py` | Usa fixtures `usuario` e `client_autenticado` do `conftest.py` |
| Fixtures | `conftest.py` | `usuario` (User) e `client_autenticado` (Client logado) |

### Restrições
- Não criar novas URLs
- Não criar novos models
- Usar `select_related` para evitar N+1
- Manter design dark mode existente (glass cards, Tailwind)
- Texto da UI em português

---

## Checklist de Execução

### Backend

#### 1. Selector — `get_transactions_by_account`
- [ ] Ler skill `django-patterns`
- [ ] **RED** — Escrever testes em `finances/tests.py`:
  - `test_get_transactions_by_account_retorna_ultimas_5` — cria 7 transações, verifica que retorna apenas 5
  - `test_get_transactions_by_account_ordena_por_data_desc` — verifica ordenação
  - `test_get_transactions_by_account_filtra_por_conta` — cria transações em 2 contas, verifica isolamento
  - `test_get_transactions_by_account_filtra_por_usuario` — outro usuário não vê transações
  - `test_get_transactions_by_account_limit_customizado` — passa `limit=3`, verifica
  - `test_get_transactions_by_account_conta_sem_transacoes` — retorna queryset vazio
  - `test_get_transactions_by_account_usa_select_related` — verifica que `categoria` e `conta` estão no `select_related` (via `assertNumQueries` ou inspecionando queryset)
- [ ] Rodar testes → todos falham (RED confirmado)
- [ ] **GREEN** — Implementar `get_transactions_by_account(account_id, user, limit=5)` em `finances/selectors.py`:
  ```python
  def get_transactions_by_account(account_id: int, user, limit: int = 5):
      return (
          Transaction.objects
          .filter(conta_id=account_id, usuario=user)
          .select_related('categoria', 'conta')
          .order_by('-data')[:limit]
      )
  ```
- [ ] Rodar testes → todos passam (GREEN confirmado)
- [ ] **REFACTOR** — Revisar com checklist `code-review`

#### 2. View — `ContaCorrenteListView.get_context_data`
- [ ] **RED** — Escrever testes de view em `finances/tests.py`:
  - `test_conta_corrente_list_context_contas_com_transacoes` — verifica que `contas_com_saldo` agora inclui transações como terceiro elemento da tupla (ou dict)
  - `test_conta_corrente_list_transacoes_no_template` — usa `client_autenticado`, GET na rota, verifica que descrição de transação aparece no HTML response
- [ ] Rodar testes → falham (RED confirmado)
- [ ] **GREEN** — Modificar `get_context_data` em `finances/views.py` L299-305:
  - Mudar a tupla `(conta, saldo)` para `(conta, saldo, transacoes)` incluindo chamada ao novo selector
  ```python
  def get_context_data(self, **kwargs):
      ctx = super().get_context_data(**kwargs)
      ctx['contas_com_saldo'] = [
          (
              conta,
              selectors.get_account_balance(conta.pk, self.request.user),
              selectors.get_transactions_by_account(conta.pk, self.request.user),
          )
          for conta in ctx['contas']
      ]
      return ctx
  ```
- [ ] Rodar testes → passam (GREEN confirmado)
- [ ] **REFACTOR** — Avaliar N+1: cada conta faz 1 query para saldo + 1 para transações. Aceitável para poucas contas; documentar como risco se escalar.
- [ ] Executar `code-review`

#### 3. Commit Backend
- [ ] Ler skill `git-workflow`
- [ ] Commit: `feat(finances): add transactions per account selector and view context`

### Frontend

#### 4. Template — Transações dentro do card
- [ ] Ler skills `frontend-finance-design` e `htmx-patterns`
- [ ] Modificar `finances/templates/finances/conta_corrente_list.html`:
  - Após o bloco de saldo (L63 `R$ {{ saldo|floatformat:"2g" }}`), adicionar seção de transações
  - Atualizar o loop `{% for conta, saldo in contas_com_saldo %}` → `{% for conta, saldo, transacoes in contas_com_saldo %}`
  - Estrutura do bloco de transações:
    ```html
    {% if transacoes %}
    <div class="mt-4 pt-3 border-t border-zinc-700/50">
      <p class="text-xs text-zinc-500 font-medium mb-2">Últimas transações</p>
      <ul class="space-y-1.5">
        {% for tx in transacoes %}
        <li class="flex items-center justify-between text-xs">
          <div class="flex items-center gap-2 min-w-0 flex-1">
            <span class="w-1.5 h-1.5 rounded-full shrink-0
              {% if tx.tipo == 'entrada' %}bg-green-400{% else %}bg-red-400{% endif %}">
            </span>
            <span class="text-zinc-300 truncate">{{ tx.descricao }}</span>
          </div>
          <div class="flex items-center gap-2 shrink-0 ml-2">
            <span class="text-zinc-500">{{ tx.data|date:"d/m" }}</span>
            <span class="font-medium
              {% if tx.tipo == 'entrada' %}text-green-400{% else %}text-red-400{% endif %}">
              {% if tx.tipo == 'entrada' %}+{% else %}-{% endif %}R$ {{ tx.valor|floatformat:"2g" }}
            </span>
          </div>
        </li>
        {% endfor %}
      </ul>
    </div>
    {% endif %}
    ```
- [ ] Validar responsividade: testar em viewports 320px, 768px, 1280px
- [ ] Validar acessibilidade: cores com contraste suficiente, `aria-label` se necessário
- [ ] Validar dark mode: consistente com glass cards existentes

#### 5. Commit Frontend
- [ ] Commit: `feat(finances): display last transactions in account cards`

### Testes

#### 6. Testes Unitários e de Integração
- [ ] Todos os testes do selector passando
- [ ] Todos os testes da view passando
- [ ] Rodar `pytest finances/` — sem falhas
- [ ] Rodar `pytest` (suite completa) — sem regressões

#### 7. Testes E2E (Playwright) — se infra disponível
- [ ] Ler skill `playwright-automation`
- [ ] Teste E2E: navegar para `/financas/conta-corrente/`, verificar que transações aparecem dentro dos cards
- [ ] Teste E2E: conta sem transações não exibe seção de transações

### Dependências
- [ ] `requirements/requirements.txt` atualizado (não aplicável — sem novas dependências)

### Documentação
- [ ] README Curator invocado (se alteração significativa na UI)

---

## Riscos e Premissas

| Tipo | Descrição | Mitigação |
|---|---|---|
| Risco | N+1 queries: cada conta gera 2 queries extras (saldo + transações) | Aceitável para < 20 contas. Se escalar, usar `Prefetch` no queryset da view |
| Risco | Cards ficarem muito altos com 5 transações em telas pequenas | Limitar a 3 em mobile via CSS `hidden` ou reduzir `limit` |
| Premissa | Transaction sempre tem `conta` preenchida para contas correntes | Se `conta` for NULL, transação não aparece (comportamento correto do filtro) |
| Premissa | O loop do template aceita desempacotamento de 3 valores | Django template `{% for a, b, c in lista %}` suporta tuplas de 3 |

---

## Log de Progresso
- 2026-03-25: Plano criado com análise do código existente (view L287-306, selector, template, models)

---

## Validação Final
- [ ] Todos os itens do checklist marcados
- [ ] Testes passando (`pytest finances/` e suite completa)
- [ ] README atualizado (se aplicável)
- [ ] Sem itens bloqueados
