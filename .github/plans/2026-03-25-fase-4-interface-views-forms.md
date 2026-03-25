# Plano: Fase 4 — Interface, Views e Forms

**Data:** 2026-03-25
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Implementar a camada de interface da app `finances`: Forms validados com Tailwind, Views CBV enxutas que orquestram services/selectors, e templates dark-mode mobile-first para transações e categorias.

---

## Escopo

### Incluido
- `finances/forms.py`: `TransactionForm` e `CategoryForm` (ModelForms com classes CSS Tailwind e choices filtradas por usuário)
- `finances/views.py`: 8 views CBV com `LoginRequiredMixin` (List, Create, Update, Delete para Transaction e Category)
- 5 templates financeiros em `finances/templates/finances/`
- Testes de integração: autenticação, isolamento de dados por usuário, fluxos CRUD

### Fora de escopo
- Lógica de negócio nas views (pertence aos services/selectors da Fase 3)
- Integração com dashboard e gráficos (Fase 5)
- Relatórios e exportação
- API REST / endpoints JSON

---

## Checklist de Execucao

### 0. Preparacao
- [ ] Ler skill `django-patterns` (`SKILL.md`)
- [ ] Ler skill `frontend-finance-design` (`SKILL.md`)
- [ ] Ler skill `htmx-patterns` (`SKILL.md`)
- [ ] Ler skill `testing-workflow` (`SKILL.md`)
- [ ] Confirmar que Fase 3 (services + selectors) está concluída e testes passando

---

### 1. Forms — TDD (RED → GREEN)

#### 1.1 TransactionForm
- [ ] **RED** — Escrever testes em `finances/tests.py`:
  - `test_transaction_form_valid_data` — form válido com todos os campos obrigatórios
  - `test_transaction_form_missing_required_fields` — form inválido sem valor/data/tipo
  - `test_transaction_form_conta_choices_filtered_by_user` — choices de `conta` só exibem contas do usuário autenticado
  - `test_transaction_form_categoria_choices_filtered_by_user` — choices de `categoria` só exibem categorias do usuário
  - `test_transaction_form_tailwind_classes_present` — campos possuem classes CSS configuradas
- [ ] **GREEN** — Implementar `TransactionForm` em `finances/forms.py`:
  - `ModelForm` para `Transaction`
  - Campos: `valor`, `data`, `tipo`, `descricao`, `categoria`, `conta`
  - `__init__` recebe `user` e filtra querysets de `categoria` e `conta` por `user`
  - Widgets com classes Tailwind (input, select, textarea)
- [ ] Confirmar todos os testes passando

#### 1.2 CategoryForm
- [ ] **RED** — Escrever testes:
  - `test_category_form_valid_data` — form válido com nome e tipo
  - `test_category_form_missing_name` — form inválido sem nome
  - `test_category_form_keywords_optional` — keywords é opcional
  - `test_category_form_tailwind_classes_present` — classes CSS presentes
  - `test_category_form_help_text_present` — help text configurado em ao menos um campo
- [ ] **GREEN** — Implementar `CategoryForm` em `finances/forms.py`:
  - `ModelForm` para `Category`
  - Campos: `nome`, `tipo`, `keywords`
  - Widgets com classes Tailwind
  - `help_text` em `keywords` explicando formato
- [ ] Confirmar todos os testes passando

---

### 2. Views — TDD (RED → GREEN)

#### 2.1 TransactionListView
- [ ] **RED** — Escrever testes:
  - `test_transaction_list_view_requires_login` — GET sem autenticação retorna 302 para login
  - `test_transaction_list_view_returns_200` — GET autenticado retorna 200
  - `test_transaction_list_view_filters_by_user` — lista só contém transações do usuário autenticado
  - `test_transaction_list_view_excludes_other_user_data` — transações de outro usuário não aparecem
- [ ] **GREEN** — Implementar `TransactionListView`:
  - `LoginRequiredMixin` + `ListView`
  - `get_queryset` usa selector `get_transactions_by_user(user=self.request.user)`
  - `context_object_name = 'transactions'`
- [ ] Confirmar todos os testes passando

#### 2.2 TransactionCreateView
- [ ] **RED** — Escrever testes:
  - `test_transaction_create_view_requires_login` — GET sem auth retorna 302
  - `test_transaction_create_view_get_returns_200` — GET autenticado retorna 200
  - `test_transaction_create_view_post_valid_data_redirects` — POST válido retorna 302
  - `test_transaction_create_view_post_creates_transaction` — transação criada na base
  - `test_transaction_create_view_post_invalid_data_returns_form` — POST inválido retorna 200 com form
  - `test_transaction_create_view_form_kwargs_passes_user` — form recebe `user` como kwarg
- [ ] **GREEN** — Implementar `TransactionCreateView`:
  - `LoginRequiredMixin` + `CreateView`
  - `form_class = TransactionForm`
  - `get_form_kwargs` injeta `user=self.request.user`
  - `form_valid` chama `create_transaction(user, form.cleaned_data)` e redireciona
- [ ] Confirmar todos os testes passando

#### 2.3 TransactionUpdateView
- [ ] **RED** — Escrever testes:
  - `test_transaction_update_view_requires_login` — GET sem auth retorna 302
  - `test_transaction_update_view_returns_200` — GET autenticado retorna 200
  - `test_transaction_update_view_post_valid_data_redirects` — POST válido retorna 302
  - `test_transaction_update_view_post_updates_data` — dados atualizados na base
  - `test_transaction_update_view_other_user_cannot_edit` — usuário B não edita transação do usuário A (404)
- [ ] **GREEN** — Implementar `TransactionUpdateView`:
  - `LoginRequiredMixin` + `UpdateView`
  - `get_queryset` filtra por `user=self.request.user` (evita acesso cruzado)
  - `get_form_kwargs` injeta `user=self.request.user`
  - `form_valid` chama `update_transaction(instance, form.cleaned_data)`
- [ ] Confirmar todos os testes passando

#### 2.4 TransactionDeleteView
- [ ] **RED** — Escrever testes:
  - `test_transaction_delete_view_requires_login` — GET sem auth retorna 302
  - `test_transaction_delete_view_returns_200` — GET autenticado retorna 200 (confirmação)
  - `test_transaction_delete_view_post_deletes_and_redirects` — POST exclui e redireciona
  - `test_transaction_delete_view_other_user_cannot_delete` — usuário B não exclui transação do usuário A (404)
- [ ] **GREEN** — Implementar `TransactionDeleteView`:
  - `LoginRequiredMixin` + `DeleteView`
  - `get_queryset` filtra por `user=self.request.user`
  - `success_url` aponta para lista
- [ ] Confirmar todos os testes passando

#### 2.5 CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
- [ ] **RED** — Escrever testes para cada view (padrão análogo às Transaction views):
  - Requer login (302 sem auth)
  - GET retorna 200
  - POST válido redireciona e persiste
  - Isolamento de dados por usuário (404 para acesso cruzado)
- [ ] **GREEN** — Implementar as 4 views de Category:
  - `CategoryListView`: `get_queryset` usa selector filtrado por usuário
  - `CategoryCreateView`: `form_valid` chama `create_category`
  - `CategoryUpdateView`: `get_queryset` filtra por usuário; `form_valid` chama `update_category`
  - `CategoryDeleteView`: `get_queryset` filtra por usuário
- [ ] Confirmar todos os testes passando

---

### 3. URLs (`finances/urls.py`)
- [ ] Registrar todas as 8 rotas com `path` e `name` descritivo:
  - `transactions/` → `transaction-list`
  - `transactions/new/` → `transaction-create`
  - `transactions/<pk>/edit/` → `transaction-update`
  - `transactions/<pk>/delete/` → `transaction-delete`
  - `categories/` → `category-list`
  - `categories/new/` → `category-create`
  - `categories/<pk>/edit/` → `category-update`
  - `categories/<pk>/delete/` → `category-delete`
- [ ] Incluir `finances/urls.py` em `fintrack/urls.py`
- [ ] Confirmar que `reverse()` funciona para todas as rotas nos testes

---

### 4. Templates — Frontend (dark mode, mobile-first, Tailwind)

> Ler `frontend-finance-design` e `htmx-patterns` antes de implementar.

#### 4.1 `transaction_list.html`
- [ ] Extends `base.html`
- [ ] Cards responsivos: mobile (coluna) → desktop (tabela ou grid)
- [ ] Exibe: valor, data, tipo (badge colorido entrada/saída), categoria, ações (editar/excluir)
- [ ] Botão "Nova Transação" com destaque visual
- [ ] Estado vazio ("Nenhuma transação cadastrada") com call-to-action
- [ ] HTMX opcional: carregamento parcial da lista

#### 4.2 `transaction_form.html`
- [ ] Extends `base.html`
- [ ] Formulário estilizado com inputs, selects e labels Tailwind dark-mode
- [ ] Título dinâmico: "Nova Transação" / "Editar Transação"
- [ ] Botões: Salvar (primário) + Cancelar (secundário, link para lista)
- [ ] Exibição de erros de validação por campo (estilo visual destacado)

#### 4.3 `transaction_confirm_delete.html`
- [ ] Extends `base.html`
- [ ] Exibe dados da transação a ser excluída
- [ ] Botões: Confirmar exclusão (danger/vermelho) + Cancelar (volta para lista)

#### 4.4 `category_list.html`
- [ ] Extends `base.html`
- [ ] Lista de categorias com nome, tipo (badge) e ações
- [ ] Botão "Nova Categoria"
- [ ] Estado vazio com call-to-action

#### 4.5 `category_form.html`
- [ ] Extends `base.html`
- [ ] Formulário com campos nome, tipo, keywords
- [ ] Help text visível para o campo keywords
- [ ] Botões: Salvar + Cancelar

---

### 5. Testes de Integracao (Fluxo End-to-End)

- [ ] **RED** → **GREEN** — Fluxos completos:
  - `test_create_transaction_flow` — login → GET form → POST válido → redireciona → item aparece na lista
  - `test_update_transaction_flow` — login → GET form editando transação existente → POST → atualizado na lista
  - `test_delete_transaction_flow` — login → GET confirmação → POST → removido da lista
  - `test_create_category_flow` — login → GET form → POST → aparece na lista
  - `test_unauthenticated_all_routes_redirect_to_login` — todas as 8 rotas retornam 302 sem auth
  - `test_user_isolation` — user_a não vê/edita/exclui dados de user_b em nenhuma rota

---

### 6. Code Review
- [ ] Ler skill `code-review` e aplicar checklist
- [ ] Sem imports não utilizados em `forms.py` e `views.py`
- [ ] Nenhuma lógica de negócio dentro das views (apenas orquestração)
- [ ] Sem query N+1 nos `get_queryset` das views
- [ ] Sem dados de outro usuário vazando em nenhum contexto de template
- [ ] PEP 8 cumprido (`flake8` ou `ruff`)

---

### 7. Commit com Git Workflow
- [ ] Ler skill `git-workflow`
- [ ] Stage apenas arquivos da Fase 4
- [ ] Commit com mensagem Conventional Commits:
  ```
  feat(finances): add forms, CBV views and templates for transactions and categories
  ```
- [ ] Push seguro (sem `--force`)

---

## Riscos e Premissas

- **Risco:** Services/selectors da Fase 3 podem não estar implementados → bloqueio nas views
- **Risco:** Choices filtradas por usuário exigem que o form receba `user` explicitamente — CBVs devem sobrescrever `get_form_kwargs`
- **Risco:** Acesso cruzado entre usuários deve ser bloqueado em `get_queryset` das views de Update/Delete; falha aqui é vulnerabilidade de segurança (OWASP: Broken Access Control)
- **Premissa:** `Transaction` e `Category` possuem FK para `User` já definidas nas migrations da Fase 2
- **Premissa:** `base.html` com Tailwind CDN já existe em `core/templates/base.html`
- **Premissa:** `finances/urls.py` ainda não existe e precisa ser criado

---

## Log de Progresso

- 2026-03-25: Plano criado — Fase 4 (Interface, Views e Forms)

---

## Validacao Final

- [ ] Todos os itens do checklist marcados como `[x]`
- [ ] `pytest` sem falhas (unitários + integração)
- [ ] Nenhum dado de usuário A acessível pelo usuário B
- [ ] Templates renderizam sem erro em mobile e desktop
- [ ] README atualizado (se aplicável)
- [ ] Sem itens bloqueados
