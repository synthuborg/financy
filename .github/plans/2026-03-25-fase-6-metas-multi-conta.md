# Plano: Fase 6 — Metas Financeiras e Multi-Conta

**Data:** 2026-03-25
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Implementar o modelo `Goal` (Meta Financeira) com CRUD completo, adicionar CRUD de Contas (`Account`) e integrar resumo de metas ao Dashboard — mantendo Clean Architecture (Views → Services/Selectors → Models) e terminologia inviolável Entradas/Saídas.

---

## Escopo

### Incluído
- Model `Goal` em `finances/models.py` com properties `percentual_concluido` e `saldo_restante`
- Services: `create_goal`, `update_goal`, `delete_goal`, `add_progress_to_goal`
- Selectors: `get_all_goals`, `get_goal_by_id`
- CRUD de Contas (4 CBVs + `AccountForm` + 3 templates + 4 URLs)
- CRUD de Metas (5 CBVs + `GoalForm` + 4 templates + 5 URLs)
- Seletor `obter_metas_resumo(user)` em `dashboard/selectors.py`
- Card de Metas no dashboard com barra de progresso (HTMX + Tailwind)
- Migração `0003_goal.py` para o novo model
- Testes unitários e de integração para cada entrega
- Navegação atualizada no `base.html`

### Fora de Escopo
- Upload de extratos (Fase 2, já implementado)
- Relatórios / exportação (Fase 7)
- Cartão de crédito avançado (Fase 7)
- Gráfico de investimentos real (Fase 7)

---

## Checklist de Execução

### 0. Preparação
- [ ] Ler skill `django-patterns` antes de criar models/CBVs
- [ ] Ler skill `frontend-finance-design` antes de criar templates
- [ ] Ler skill `htmx-patterns` antes de implementar interações HTMX
- [ ] Ler skill `testing-workflow` antes de escrever testes
- [ ] Verificar estado atual de `finances/models.py`, `finances/services.py`, `finances/selectors.py`
- [ ] Verificar `finances/urls.py` e `finances/views.py` para não duplicar padrões
- [ ] Confirmar que 104 testes existentes continuam passando (`pytest`)

---

### 1. Model `Goal` — RED → GREEN

#### 1a. Testes (RED)
- [ ] Criar testes em `finances/tests.py` para `Goal`:
  - [ ] `test_goal_str` — representação string do model
  - [ ] `test_percentual_concluido_zero` — valor_atual=0, valor_alvo=200 → 0%
  - [ ] `test_percentual_concluido_parcial` — valor_atual=50, valor_alvo=200 → 25%
  - [ ] `test_percentual_concluido_completo` — valor_atual=200, valor_alvo=200 → 100%
  - [ ] `test_saldo_restante` — valor_alvo - valor_atual
  - [ ] `test_saldo_restante_zero_quando_completo`
  - [ ] `test_goal_usuario_fk` — meta pertence ao usuário correto
  - [ ] `test_goal_categoria_nullable` — pode ser criada sem categoria
  - [ ] `test_goal_prazo_nullable` — pode ser criada sem prazo
- [ ] Executar `pytest finances/tests.py -k goal` → confirmar FALHA (RED)

#### 1b. Implementação (GREEN)
- [ ] Adicionar model `Goal` em `finances/models.py`:
  ```python
  class Goal(models.Model):
      titulo = models.CharField(max_length=200)
      valor_alvo = models.DecimalField(max_digits=10, decimal_places=2)
      valor_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
      prazo = models.DateField(null=True, blank=True)
      usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
      categoria = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

      @property
      def percentual_concluido(self) -> int:
          if self.valor_alvo <= 0:
              return 0
          return min(int((self.valor_atual / self.valor_alvo) * 100), 100)

      @property
      def saldo_restante(self):
          return max(self.valor_alvo - self.valor_atual, 0)

      def __str__(self):
          return self.titulo
  ```
- [ ] Registrar `Goal` em `finances/admin.py`
- [ ] Gerar migração: `python manage.py makemigrations finances` → `0003_goal.py`
- [ ] Aplicar migração: `python manage.py migrate`
- [ ] Executar `pytest finances/tests.py -k goal` → confirmar PASSA (GREEN)

---

### 2. Services para `Goal` — RED → GREEN

#### 2a. Testes (RED)
- [ ] Criar testes em `finances/tests.py` para services de Goal:
  - [ ] `test_create_goal_valido` — cria meta com dados corretos
  - [ ] `test_create_goal_valor_alvo_zero_raises` — valor_alvo=0 → `ValueError`
  - [ ] `test_create_goal_valor_alvo_negativo_raises` — valor_alvo<0 → `ValueError`
  - [ ] `test_update_goal_proprio_usuario` — atualiza dados
  - [ ] `test_update_goal_outro_usuario_raises` — escopo por usuário → 404
  - [ ] `test_delete_goal_proprio_usuario` — remove meta
  - [ ] `test_delete_goal_outro_usuario_raises` — escopo por usuário → 404
  - [ ] `test_add_progress_to_goal_incrementa` — soma valor ao valor_atual
  - [ ] `test_add_progress_nao_excede_valor_alvo` — trava em valor_alvo
  - [ ] `test_add_progress_valor_negativo_raises` — valor ≤ 0 → `ValueError`
- [ ] Executar `pytest finances/tests.py -k service_goal` → confirmar FALHA (RED)

#### 2b. Implementação (GREEN)
- [ ] Adicionar em `finances/services.py`:
  - [ ] `create_goal(user, data) -> Goal`
  - [ ] `update_goal(goal_id, user, data) -> Goal`
  - [ ] `delete_goal(goal_id, user) -> None`
  - [ ] `add_progress_to_goal(goal_id, user, valor) -> Goal`
- [ ] Executar `pytest finances/tests.py -k service_goal` → confirmar PASSA (GREEN)

---

### 3. Selectors para `Goal` — RED → GREEN

#### 3a. Testes (RED)
- [ ] Criar testes em `finances/tests.py` para selectors de Goal:
  - [ ] `test_get_all_goals_retorna_apenas_do_usuario` — isolamento por usuário
  - [ ] `test_get_all_goals_ordenado_por_prazo` — order_by prazo
  - [ ] `test_get_goal_by_id_proprio_usuario` — retorna a meta correta
  - [ ] `test_get_goal_by_id_outro_usuario_404` — get_object_or_404 scope
- [ ] Executar `pytest finances/tests.py -k selector_goal` → confirmar FALHA (RED)

#### 3b. Implementação (GREEN)
- [ ] Adicionar em `finances/selectors.py`:
  - [ ] `get_all_goals(user) -> QuerySet`
  - [ ] `get_goal_by_id(goal_id, user) -> Goal`
- [ ] Executar `pytest finances/tests.py -k selector_goal` → confirmar PASSA (GREEN)

---

### 4. CRUD de Contas (`Account`) — RED → GREEN

#### 4a. Testes (RED)
- [ ] Criar testes em `finances/tests.py` para CRUD de Contas:
  - [ ] `test_account_list_view_autenticado` — 200, lista contas do usuário
  - [ ] `test_account_list_view_anonimo_redireciona` — 302 → login
  - [ ] `test_account_create_view_get` — 200, formulário
  - [ ] `test_account_create_view_post_valido` — cria conta, redireciona
  - [ ] `test_account_create_view_post_invalido` — 200, erros no form
  - [ ] `test_account_update_view_proprio_usuario` — atualiza conta
  - [ ] `test_account_update_view_outro_usuario_404`
  - [ ] `test_account_delete_view_proprio_usuario` — remove conta
  - [ ] `test_account_delete_view_outro_usuario_404`
- [ ] Executar `pytest finances/tests.py -k account` → confirmar FALHA (RED)

#### 4b. Implementação (GREEN)
- [ ] Criar `AccountForm` em `finances/forms.py` (campos: `nome`, `tipo`)
- [ ] Adicionar em `finances/views.py`:
  - [ ] `AccountListView(LoginRequiredMixin, ListView)`
  - [ ] `AccountCreateView(LoginRequiredMixin, CreateView)`
  - [ ] `AccountUpdateView(LoginRequiredMixin, UpdateView)`
  - [ ] `AccountDeleteView(LoginRequiredMixin, DeleteView)`
- [ ] Adicionar 4 URLs em `finances/urls.py`:
  ```
  accounts/              → AccountListView     (name='account-list')
  accounts/create/       → AccountCreateView   (name='account-create')
  accounts/<pk>/update/  → AccountUpdateView   (name='account-update')
  accounts/<pk>/delete/  → AccountDeleteView   (name='account-delete')
  ```
- [ ] Criar templates em `finances/templates/finances/`:
  - [ ] `account_list.html` — lista com botões Editar/Excluir, Tailwind dark mode
  - [ ] `account_form.html` — formulário de criação/edição
  - [ ] `account_confirm_delete.html` — confirmação de exclusão
- [ ] Executar `pytest finances/tests.py -k account` → confirmar PASSA (GREEN)

---

### 5. CRUD de Metas (`Goal`) — RED → GREEN

#### 5a. Testes (RED)
- [ ] Criar testes em `finances/tests.py` para CRUD de Metas:
  - [ ] `test_goal_list_view_autenticado` — 200, lista metas do usuário
  - [ ] `test_goal_list_view_anonimo_redireciona` — 302 → login
  - [ ] `test_goal_create_view_get` — 200, formulário
  - [ ] `test_goal_create_view_post_valido` — cria meta, redireciona
  - [ ] `test_goal_create_view_post_invalido` — 200, erros no form
  - [ ] `test_goal_update_view_proprio_usuario`
  - [ ] `test_goal_update_view_outro_usuario_404`
  - [ ] `test_goal_delete_view_proprio_usuario`
  - [ ] `test_goal_delete_view_outro_usuario_404`
  - [ ] `test_goal_add_progress_view_post_valido` — incrementa valor_atual
  - [ ] `test_goal_add_progress_view_valor_invalido` — exibe erro
- [ ] Executar `pytest finances/tests.py -k goal_view` → confirmar FALHA (RED)

#### 5b. Implementação (GREEN)
- [ ] Criar `GoalForm` em `finances/forms.py` (campos: `titulo`, `valor_alvo`, `prazo`, `categoria`)
- [ ] Criar `GoalAddProgressForm` em `finances/forms.py` (campo: `valor`)
- [ ] Adicionar em `finances/views.py`:
  - [ ] `GoalListView(LoginRequiredMixin, ListView)`
  - [ ] `GoalCreateView(LoginRequiredMixin, CreateView)`
  - [ ] `GoalUpdateView(LoginRequiredMixin, UpdateView)`
  - [ ] `GoalDeleteView(LoginRequiredMixin, DeleteView)`
  - [ ] `GoalAddProgressView(LoginRequiredMixin, View)` — POST only
- [ ] Adicionar 5 URLs em `finances/urls.py`:
  ```
  goals/                   → GoalListView         (name='goal-list')
  goals/create/            → GoalCreateView        (name='goal-create')
  goals/<pk>/update/       → GoalUpdateView        (name='goal-update')
  goals/<pk>/delete/       → GoalDeleteView        (name='goal-delete')
  goals/<pk>/add-progress/ → GoalAddProgressView   (name='goal-add-progress')
  ```
- [ ] Criar templates em `finances/templates/finances/`:
  - [ ] `goal_list.html` — cards com barra de progresso, cor emerald se 100%, Tailwind dark mode
  - [ ] `goal_form.html` — formulário com datepicker para `prazo`
  - [ ] `goal_confirm_delete.html` — confirmação de exclusão
  - [ ] `goal_add_progress.html` — modal/fragmento HTMX para adicionar progresso
- [ ] Executar `pytest finances/tests.py -k goal_view` → confirmar PASSA (GREEN)

---

### 6. Dashboard — Resumo de Metas

#### 6a. Testes (RED)
- [ ] Criar testes em `dashboard/tests.py`:
  - [ ] `test_obter_metas_resumo_retorna_top3` — retorna no máximo 3 metas
  - [ ] `test_obter_metas_resumo_escopo_usuario` — isolamento por usuário
  - [ ] `test_obter_metas_resumo_percentual_correto` — valores calculados
  - [ ] `test_dashboard_view_contem_metas` — context tem `metas_resumo`
- [ ] Executar `pytest dashboard/tests.py -k metas` → confirmar FALHA (RED)

#### 6b. Implementação (GREEN)
- [ ] Adicionar `obter_metas_resumo(user) -> list[dict]` em `dashboard/selectors.py`:
  - Retorna top 3 metas do usuário ordenadas por `prazo` (nulls last)
  - Cada dict: `id`, `titulo`, `percentual`, `valor_atual`, `valor_alvo`, `saldo_restante`
- [ ] Atualizar `dashboard/views.py` para incluir `metas_resumo` no contexto
- [ ] Atualizar `dashboard/templates/dashboard/fragmentos/grafico_metas.html`:
  - Cards de metas com barra de progresso Tailwind (`bg-emerald-500`)
  - Exibir título, progresso percentual, valor atual / valor alvo
  - Link "Ver todas" → `goal-list`
  - Se não há metas: mensagem vazia com CTA para criar
- [ ] Executar `pytest dashboard/tests.py -k metas` → confirmar PASSA (GREEN)

---

### 7. Navegação e UX

- [ ] Atualizar `core/templates/base.html`:
  - [ ] Adicionar link **Contas** → `finances:account-list` no menu lateral
  - [ ] Adicionar link **Metas** → `finances:goal-list` no menu lateral
- [ ] Verificar responsividade mobile dos novos templates (seguir `frontend-finance-design`)
- [ ] Confirmar que terminologia Entradas/Saídas não foi alterada em nenhum template

---

### 8. Code Review

- [ ] Ler skill `code-review`
- [ ] Verificar: sem código duplicado entre services e views
- [ ] Verificar: sem imports não utilizados em todos os arquivos modificados
- [ ] Verificar: CBVs não contêm lógica de negócio (delegar para services/selectors)
- [ ] Verificar: `LoginRequiredMixin` em todos os CBVs do CRUD
- [ ] Verificar: escopo por `usuario` em todas as queries (sem vazamento entre usuários)
- [ ] Verificar: PEP 8 em todo código novo
- [ ] Verificar: nenhum `print()` ou `console.log()` de debug

---

### 9. Testes Finais e Regressão

- [ ] Executar suite completa: `pytest` → todos os testes passando (≥ 130 testes)
- [ ] Confirmar que os 104 testes anteriores continuam passando
- [ ] Executar `pytest --tb=short` e resolver qualquer falha

---

### 10. Dependencies

- [ ] Verificar se há novas dependências em `requirements/requirements.txt` (não esperado nessa fase)
- [ ] Confirmar que migração `0003_goal.py` está comitada junto com o código

---

### 11. Git e Commit

- [ ] Ler skill `git-workflow`
- [ ] Stagear arquivos modificados/criados:
  - `finances/models.py`, `finances/migrations/0003_goal.py`
  - `finances/services.py`, `finances/selectors.py`
  - `finances/forms.py`, `finances/views.py`, `finances/urls.py`
  - `finances/admin.py`
  - `finances/tests.py`
  - Templates de `finances/` (account e goal)
  - `dashboard/selectors.py`, `dashboard/views.py`
  - `dashboard/templates/dashboard/fragmentos/grafico_metas.html`
  - `core/templates/base.html`
  - `.github/plans/2026-03-25-fase-6-metas-multi-conta.md`
- [ ] Commit seguindo Conventional Commits:
  ```
  feat(finances): add Goal model, Account CRUD, and Goal CRUD (Fase 6)
  ```
- [ ] Push para branch `feat/fase-6-metas-multi-conta`

---

## Riscos e Premissas

- **Risco:** `Account` já tem FK em `Transaction` — CRUD de contas deve preservar integridade referencial (usar `PROTECT` ou confirmar comportamento no delete)
- **Risco:** Migração pode conflitar se houver branch paralela com migrações pendentes — verificar antes de `makemigrations`
- **Premissa:** `settings.AUTH_USER_MODEL` está configurado e funcional (confirmado pelo estado atual)
- **Premissa:** Tailwind CDN e HTMX CDN já estão importados no `base.html` — não adicionar dependências JS extras
- **Premissa:** `finances/selectors.py` já existe com seletores de Transaction/Category — Goal segue o mesmo padrão
- **Risco:** `GoalAddProgressView` é um endpoint POST puro — garantir proteção CSRF e não expor como GET

---

## Log de Progresso

- 2026-03-25: Plano criado. Escopo definido para Model Goal, CRUD Contas, CRUD Metas e integração Dashboard.

---

## Validação Final

- [ ] Todos os itens do checklist marcados `[x]`
- [ ] Suite de testes passando (≥ 130 testes, zero falhas)
- [ ] Navegação: links Contas e Metas no menu lateral
- [ ] Dashboard: card de metas com barra de progresso visível
- [ ] Sem vazamento de dados entre usuários (escopo garantido)
- [ ] Terminologia Entradas/Saídas intacta em todos os templates
- [ ] Commit realizado na branch correta
- [ ] Sem `print()`, `TODO` críticos ou código morto no diff
