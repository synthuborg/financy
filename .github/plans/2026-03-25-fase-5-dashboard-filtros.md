# Plano: Fase 5 — Dashboard com calculate_balance e Filtros

**Data:** 2026-03-25
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Conectar o `DashboardView` ao serviço `calculate_balance`, adicionar cards de KPI (Entradas/Saídas/Saldo do mês), tabela de atividade recente e filtros de período/tipo em `TransactionListView`.

---

## Escopo

### Incluído
- `DashboardView` passa `saldo`, `resumo_mes` e `ultimas_transacoes` ao template
- Novo seletor `obter_resumo_mes_atual(user)` em `dashboard/selectors.py`
- Novo seletor `obter_ultimas_transacoes(user, limit=5)` em `dashboard/selectors.py`
- Filtros GET em `TransactionListView`: `?tipo=entrada|saida`, `?data_inicio=YYYY-MM-DD`, `?data_fim=YYYY-MM-DD`
- Template `dashboard/dashboard.html` — 3 cards KPI + tabela atividade recente
- Template `finances/transaction_list.html` — formulário de filtros com HTMX
- Sidebar/navbar com links para `/financas/transacoes/` e `/financas/categorias/`

### Fora de Escopo
- Metas e investimentos (Fase 6)
- Multi-conta (Fase 6)
- Exportação de relatórios (Fase 7)
- Upload de extratos (Fase 2, já implementado)

---

## Checklist de Execução

### 1. Leitura de Skills (pre-work)
- [ ] Ler `django-patterns` SKILL — confirmar convenções CBV, selectors, services
- [ ] Ler `frontend-finance-design` SKILL — confirmar paleta Tailwind (emerald = Entradas, red = Saídas)
- [ ] Ler `htmx-patterns` SKILL — confirmar padrão fragmento HTMX para filtros
- [ ] Ler `testing-workflow` SKILL — confirmar estratégia de testes antes de implementar

---

### 2. Seletores — `dashboard/selectors.py`

#### RED (testes primeiro)
- [ ] Criar testes em `dashboard/tests.py`:
  - `test_obter_resumo_mes_atual_retorna_zeros_sem_transacoes()`
  - `test_obter_resumo_mes_atual_soma_apenas_mes_corrente()`
  - `test_obter_resumo_mes_atual_separa_entradas_e_saidas()`
  - `test_obter_resumo_mes_atual_calcula_saldo_liquido_correto()`
  - `test_obter_ultimas_transacoes_retorna_limite_correto()`
  - `test_obter_ultimas_transacoes_ordena_por_data_decrescente()`
  - `test_obter_ultimas_transacoes_isolado_por_usuario()`
- [ ] Confirmar que todos os novos testes **falham** (RED)

#### GREEN (implementação)
- [ ] Implementar `obter_resumo_mes_atual(user)` em `dashboard/selectors.py`:
  - Filtra `Transaction` por `usuario=user`, `tipo='entrada'`, `data__gte=inicio_mes`
  - Filtra `Transaction` por `usuario=user`, `tipo='saida'`, `data__gte=inicio_mes`
  - Usa `Sum('valor')` ou `0` com `or Decimal('0')`
  - Retorna `{'total_entradas': Decimal, 'total_saidas': Decimal, 'saldo_liquido': Decimal}`
- [ ] Implementar `obter_ultimas_transacoes(user, limit=5)` em `dashboard/selectors.py`:
  - `Transaction.objects.filter(usuario=user).select_related('categoria').order_by('-data')[:limit]`
- [ ] Confirmar que todos os testes do passo RED **passam** (GREEN)

---

### 3. `DashboardView` — `dashboard/views.py`

#### RED (testes primeiro)
- [ ] Criar testes em `dashboard/tests.py`:
  - `test_dashboard_view_requer_login()`
  - `test_dashboard_view_retorna_200_usuario_autenticado()`
  - `test_dashboard_view_context_contem_resumo_mes()`
  - `test_dashboard_view_context_contem_ultimas_transacoes()`
  - `test_dashboard_view_context_contem_saldo_total()`
- [ ] Confirmar que todos os novos testes **falham** (RED)

#### GREEN (implementação)
- [ ] Atualizar `DashboardView.get_context_data()` em `dashboard/views.py`:
  ```python
  from finances.services import calculate_balance
  from . import selectors

  def get_context_data(self, **kwargs):
      ctx = super().get_context_data(**kwargs)
      ctx['saldo'] = calculate_balance(self.request.user)
      ctx['resumo_mes'] = selectors.obter_resumo_mes_atual(self.request.user)
      ctx['ultimas_transacoes'] = selectors.obter_ultimas_transacoes(self.request.user)
      return ctx
  ```
- [ ] Confirmar que todos os testes do passo RED **passam** (GREEN)

---

### 4. Filtros em `TransactionListView` — `finances/views.py`

#### RED (testes primeiro)
- [ ] Criar testes em `finances/tests.py`:
  - `test_transaction_list_filtro_tipo_entrada_retorna_apenas_entradas()`
  - `test_transaction_list_filtro_tipo_saida_retorna_apenas_saidas()`
  - `test_transaction_list_filtro_data_inicio_exclui_anteriores()`
  - `test_transaction_list_filtro_data_fim_exclui_posteriores()`
  - `test_transaction_list_filtro_combinado_tipo_e_periodo()`
  - `test_transaction_list_sem_filtro_retorna_todos()`
  - `test_transaction_list_filtro_nao_vaza_dados_entre_usuarios()`
- [ ] Confirmar que todos os novos testes **falham** (RED)

#### GREEN (implementação)
- [ ] Atualizar `TransactionListView.get_queryset()` em `finances/views.py`:
  ```python
  def get_queryset(self):
      qs = selectors.get_all_transactions(self.request.user)
      tipo = self.request.GET.get('tipo', '').strip()
      data_inicio = self.request.GET.get('data_inicio', '').strip()
      data_fim = self.request.GET.get('data_fim', '').strip()

      if tipo in ('entrada', 'saida'):
          qs = qs.filter(tipo=tipo)
      if data_inicio:
          qs = qs.filter(data__gte=data_inicio)
      if data_fim:
          qs = qs.filter(data__lte=data_fim)
      return qs
  ```
- [ ] Adicionar `get_context_data()` para repassar parâmetros ao template (preservar valores nos inputs):
  ```python
  def get_context_data(self, **kwargs):
      ctx = super().get_context_data(**kwargs)
      ctx['filtro_tipo'] = self.request.GET.get('tipo', '')
      ctx['filtro_data_inicio'] = self.request.GET.get('data_inicio', '')
      ctx['filtro_data_fim'] = self.request.GET.get('data_fim', '')
      return ctx
  ```
- [ ] Confirmar que todos os testes do passo RED **passam** (GREEN)

---

### 5. Template — `dashboard/dashboard.html`

- [ ] Adicionar 3 cards KPI no topo do template:
  - **Card Entradas do Mês** — cor `emerald` — `{{ resumo_mes.total_entradas }}`
  - **Card Saídas do Mês** — cor `red` — `{{ resumo_mes.total_saidas }}`
  - **Card Saldo Líquido** — cor dinâmica (verde se ≥ 0, vermelho se < 0) — `{{ resumo_mes.saldo_liquido }}`
- [ ] Adicionar tabela/lista de **Atividade Recente** com as últimas 5 transações:
  - Colunas: Data | Descrição | Categoria | Tipo (badge) | Valor
  - Badge Entradas: `emerald` — Badge Saídas: `red`
  - Link "Ver todas" apontando para `/financas/transacoes/`
- [ ] Garantir que `{{ saldo.total_entradas }}`, `{{ saldo.total_saidas }}`, `{{ saldo.saldo_liquido }}` (acumulado histórico) estejam acessíveis no contexto
- [ ] Validar responsividade mobile-first (grid cols-1 → cols-3 em md)

---

### 6. Template — `finances/transaction_list.html`

- [ ] Adicionar formulário de filtros com HTMX acima da tabela:
  - Select `tipo`: Todos / Entradas / Saídas
  - Input `data_inicio` (date)
  - Input `data_fim` (date)
  - Botão "Filtrar" com `hx-get` apontando para a URL atual
  - `hx-target` na tabela de transações (fragmento ou página inteira)
- [ ] Garantir que os inputs preservem os valores dos filtros ativos (`value="{{ filtro_tipo }}"`)
- [ ] Badge colorido por `tipo`: Entradas = `emerald`, Saídas = `red`

---

### 7. Sidebar/Navbar — `core/templates/base.html`

- [ ] Verificar se links para `/financas/transacoes/` e `/financas/categorias/` já existem
- [ ] Adicionar links faltantes com destaque no item ativo (`aria-current="page"`)
- [ ] Garantir que o link do Dashboard aponte para `/dashboard/`

---

### 8. Code Review
- [ ] Ler skill `code-review`
- [ ] Verificar: sem imports não usados, sem dead code, sem comentários desnecessários
- [ ] Verificar: nenhuma view acessa `Transaction.objects` diretamente (sempre via selector/service)
- [ ] Verificar: terminologia — NUNCA usar "receita" ou "despesa" (somente **Entrada** / **Saída**)
- [ ] Verificar: sem queries N+1 (usar `select_related`)
- [ ] Verificar: filtros de data não aceitam strings arbitrárias sem validação implícita do ORM

---

### 9. Testes Finais
- [ ] Rodar suite completa: `pytest` — mínimo 87 testes passando + novos testes adicionados
- [ ] Confirmar cobertura dos novos seletores e view
- [ ] Confirmar que filtro não vaza dados entre usuários diferentes

---

### 10. Git
- [ ] Ler skill `git-workflow`
- [ ] `git add` nos arquivos alterados
- [ ] Commit seguindo Conventional Commits:
  ```
  feat(dashboard): conectar calculate_balance e cards KPI ao DashboardView

  - adiciona obter_resumo_mes_atual() e obter_ultimas_transacoes() em dashboard/selectors.py
  - atualiza DashboardView com contexto de saldo, resumo_mes e ultimas_transacoes
  - adiciona filtros GET (tipo, data_inicio, data_fim) em TransactionListView
  - atualiza templates dashboard e transaction_list com cards KPI e formulário de filtros
  ```

---

## Riscos e Premissas

- **Risco 1:** `calculate_balance` acumula histórico total, não apenas o mês. O novo seletor `obter_resumo_mes_atual` deve ser usado para os cards KPI (mês corrente); `calculate_balance` fica acessível para exibir o saldo histórico geral.
- **Risco 2:** Filtros de data com strings mal formatadas — o ORM Django levanta `ValueError`; tratar com `try/except` ou validação por regex simples antes de aplicar o filtro.
- **Risco 3:** HTMX no filtro pode conflitar com paginação — garantir que a URL com query params seja compatível com `paginate_by`.
- **Premissa 1:** `Transaction.tipo` já aceita exatamente `'entrada'` e `'saida'` (confirmado nas constraints do modelo).
- **Premissa 2:** Tailwind CDN está disponível no `base.html` — não adicionar `postcss` ou build step.
- **Premissa 3:** Os 87 testes existentes continuam passando após as alterações (não há quebra de contrato em selectors/services existentes).

---

## Log de Progresso

- 2026-03-25: Plano criado. Estado inicial: `DashboardView` sem contexto de saldo, `TransactionListView` sem filtros. 87 testes passando.

---

## Validação Final
- [ ] Todos os itens do checklist marcados
- [ ] `pytest` verde com ≥ 87 + N novos testes passando
- [ ] Cards KPI exibindo Entradas (emerald), Saídas (red) e Saldo Líquido corretamente
- [ ] Filtros funcionando em `/financas/transacoes/?tipo=entrada&data_inicio=...`
- [ ] Terminologia: zero ocorrências de "receita" ou "despesa" nos arquivos alterados
- [ ] Sem itens bloqueados
