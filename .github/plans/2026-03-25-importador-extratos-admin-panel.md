# Plano: Importador de Extratos + Admin Panel Funcional

**Data:** 2026-03-25
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Implementar duas features simultâneas: (1) permitir importação de extratos bancários (CSV, PDF, OFX) diretamente na tela de transações e (2) transformar o admin panel básico num painel de gerenciamento completo com KPIs, CRUD de usuários, transações filtráveis e categorias globais.

---

## Escopo

### Incluído

**Feature 1 — Importador de Extratos**
- Botão "Importar Extrato" ao lado de "Nova Transação" em `transaction_list.html`
- Modal (Alpine.js) para upload de arquivo + seleção de conta destino
- `ImportStatementForm` (FileField + Account select)
- `ImportStatementView` (POST, LoginRequiredMixin)
- URL `finances:import_statement`
- Integração com `process_bank_statement_import()` já existente em `finances/services.py`
- Mensagem de sucesso com contagem de transações criadas/ignoradas
- Redirect para `transaction_list` após importação

**Feature 2 — Admin Panel Funcional**
- Dashboard com KPIs: total usuários, total transações, total entradas, total saídas, saldo global
- Lista de usuários com stats (nº transações, saldo) + ação ativar/desativar
- Lista de transações melhorada com filtros (tipo, data, usuário) + ação excluir
- CRUD de categorias globais (staff-only)
- Menu "Admin" condicional no sidebar (`base.html`) para `is_staff`

### Fora de escopo
- Suporte a novos formatos além de CSV, PDF, OFX
- Drag & drop no upload
- Preview/edição de transações antes de salvar (importação batch)
- Admin panel: gestão de contas/accounts de cada usuário
- Admin panel: logs de auditoria
- Admin panel: export de dados

---

## Checklist de Execução

---

### FEATURE 1 — Importador de Extratos

#### 1.1 Backend — Form (`finances/forms.py`)

- [ ] **Ler skill `django-patterns`** — confirmar padrão de forms/widgets/CSS classes
- [ ] **RED** — Escrever teste `TestImportStatementForm` em `finances/tests.py`:
  - Form válido com arquivo CSV + conta selecionada
  - Form inválido sem arquivo
  - Form inválido sem conta
  - Rejeita extensão não suportada (`.txt`, `.xlsx`)
- [ ] **GREEN** — Implementar `ImportStatementForm` em `finances/forms.py`:
  - `FileField` (accept=`.csv,.ofx,.pdf`)
  - `ModelChoiceField` para Account (filtrado por `usuario`)
  - Validação `clean_file()`: verificar extensão permitida
  - Usar `INPUT_CSS` / `SELECT_CSS` existentes
- [ ] **REFACTOR** — Revisar com skill `code-review`

#### 1.2 Backend — View (`finances/views.py`)

- [ ] **RED** — Escrever testes `TestImportStatementView` em `finances/tests.py`:
  - POST com CSV válido → redirect + mensagem sucesso + transações criadas no DB
  - POST com arquivo inválido → redirect + mensagem erro
  - POST sem autenticação → redirect login
  - POST com conta de outro usuário → erro
  - GET request → 405 (method not allowed)
- [ ] **GREEN** — Implementar `ImportStatementView` em `finances/views.py`:
  - `LoginRequiredMixin + FormView` (ou `View` com POST)
  - Chamar `process_bank_statement_import(file, user, account)`
  - `messages.success()` com contagem: "X transações importadas, Y ignoradas"
  - `messages.error()` se resultado contém erros
  - Redirect para `finances:transaction_list`
- [ ] **REFACTOR** — Revisar com skill `code-review`

#### 1.3 Backend — URL (`finances/urls.py`)

- [ ] **GREEN** — Adicionar `path('transacoes/importar/', views.ImportStatementView.as_view(), name='import_statement')`
- [ ] Verificar que testes de URL resolvem corretamente

#### 1.4 Frontend — Template (`finances/transaction_list.html`)

- [ ] **Ler skills `frontend-finance-design` e `htmx-patterns`**
- [ ] **Implementar** botão "Importar Extrato" ao lado de "Nova Transação" no header:
  - Estilo consistente (emerald/teal para diferenciar do violet do "Nova Transação")
  - Ícone upload (SVG)
  - `@click` Alpine.js para abrir modal
- [ ] **Implementar** modal Alpine.js de importação:
  - `x-data="{ open: false }"` no container
  - Overlay escuro + glass card centralizado
  - Form com `enctype="multipart/form-data"` POST para `{% url 'finances:import_statement' %}`
  - Campo file upload estilizado (dark mode)
  - Select de conta (renderizado pelo form)
  - Botão "Importar" + "Cancelar"
  - CSRF token
- [ ] **Validar** responsividade mobile (botão em stack vertical)
- [ ] **Validar** acessibilidade (labels, aria, focus trap no modal)

#### 1.5 Testes E2E (Feature 1)

- [ ] **Ler skill `testing-workflow`**
- [ ] Testes unitários/integração `pytest` passando
- [ ] _(Opcional)_ Teste E2E Playwright: upload CSV → transações aparecem na lista

#### 1.6 Commit (Feature 1)

- [ ] **Ler skill `git-workflow`**
- [ ] Commit: `feat(finances): add bank statement import (CSV/OFX/PDF)`

---

### FEATURE 2 — Admin Panel Funcional

#### 2.1 Backend — Selectors/Services (`admin_panel/`)

- [ ] **Ler skill `django-patterns`** — confirmar padrão Services/Selectors
- [ ] **RED** — Escrever testes para selectors de admin em `admin_panel/tests.py`:
  - `get_admin_kpis()` retorna dict com total_usuarios, total_transacoes, total_entradas, total_saidas, saldo_global
  - `get_all_users_with_stats()` retorna queryset com annotations (num_transacoes, saldo)
  - `get_all_transactions_admin()` retorna todas transações (sem filtro de user) com select_related
- [ ] **GREEN** — Implementar `admin_panel/selectors.py`:
  - `get_admin_kpis()` — queries agregadas
  - `get_all_users_with_stats()` — User annotate Count + Sum
  - `get_all_transactions_admin(filters)` — com filtros opcionais (tipo, data, user_id)
- [ ] **REFACTOR** — Revisar com skill `code-review`

#### 2.2 Backend — Dashboard KPIs View (`admin_panel/views.py`)

- [ ] **RED** — Escrever testes `TestAdminDashboardKPIs` em `admin_panel/tests.py`:
  - Staff vê KPIs corretos no contexto
  - KPIs com zero transações retornam Decimal('0.00')
- [ ] **GREEN** — Refatorar `AdminDashboardView` para chamar `get_admin_kpis()` e passar os KPIs no contexto
- [ ] **REFACTOR** — Revisar com skill `code-review`

#### 2.3 Backend — User List + Toggle View (`admin_panel/views.py`)

- [ ] **RED** — Escrever testes `TestAdminUserList` em `admin_panel/tests.py`:
  - Staff vê lista de todos os usuários com stats
  - Não-staff recebe 403
  - Toggle ativa/desativa usuário (POST)
  - Não pode desativar a si mesmo
- [ ] **GREEN** — Implementar:
  - `AdminUserListView(StaffRequiredMixin, ListView)` — template `admin_panel/user_list.html`
  - `AdminUserToggleView(StaffRequiredMixin, View)` — POST toggle `is_active`, redirect back
- [ ] **REFACTOR** — Revisar com skill `code-review`

#### 2.4 Backend — Transaction List melhorada (`admin_panel/views.py`)

- [ ] **RED** — Escrever testes `TestAdminTransactionListFilters` em `admin_panel/tests.py`:
  - Filtro por tipo funciona
  - Filtro por data funciona
  - Filtro por usuário funciona
  - Ação excluir remove transação (POST)
- [ ] **GREEN** — Refatorar `AdminTransactionListView`:
  - Adicionar filtros no `get_queryset()` (tipo, data_inicio, data_fim, user_id)
  - Passar filtros e lista de usuários no contexto
  - `select_related('usuario', 'categoria', 'conta')`
- [ ] **GREEN** — Implementar `AdminTransactionDeleteView(StaffRequiredMixin, View)` — POST delete
- [ ] **REFACTOR** — Revisar com skill `code-review`

#### 2.5 Backend — Category CRUD (`admin_panel/views.py`)

- [ ] **RED** — Escrever testes `TestAdminCategoryCRUD` em `admin_panel/tests.py`:
  - Staff cria categoria global (usuario=request.user como owner)
  - Staff edita categoria
  - Staff deleta categoria
  - Não-staff recebe 403 em todos os endpoints
- [ ] **GREEN** — Implementar:
  - `AdminCategoryListView(StaffRequiredMixin, ListView)`
  - `AdminCategoryCreateView(StaffRequiredMixin, CreateView)`
  - `AdminCategoryUpdateView(StaffRequiredMixin, UpdateView)`
  - `AdminCategoryDeleteView(StaffRequiredMixin, DeleteView)`
- [ ] **REFACTOR** — Revisar com skill `code-review`

#### 2.6 Backend — URLs (`admin_panel/urls.py`)

- [ ] **GREEN** — Adicionar URLs:
  - `path('usuarios/', ..., name='user_list')`
  - `path('usuarios/<int:pk>/toggle/', ..., name='user_toggle')`
  - `path('transacoes/<int:pk>/excluir/', ..., name='transaction_delete')`
  - `path('categorias/', ..., name='category_list')`
  - `path('categorias/nova/', ..., name='category_create')`
  - `path('categorias/<int:pk>/editar/', ..., name='category_update')`
  - `path('categorias/<int:pk>/excluir/', ..., name='category_delete')`

#### 2.7 Frontend — Dashboard Template (`admin_panel/templates/admin_panel/dashboard.html`)

- [ ] **Ler skills `frontend-finance-design` e `htmx-patterns`**
- [ ] **Implementar** cards de KPI:
  - Total Usuários, Total Transações, Total Entradas (verde), Total Saídas (vermelho), Saldo Global
  - Estilo glass dark mode, ícones SVG, valores formatados em R$
- [ ] **Implementar** links de navegação rápida para as subpáginas (Usuários, Transações, Categorias)

#### 2.8 Frontend — User List Template (`admin_panel/templates/admin_panel/user_list.html`)

- [ ] **Implementar** tabela/lista de usuários:
  - Colunas: username, email, nº transações, saldo, status (ativo/inativo)
  - Botão toggle ativar/desativar (POST com CSRF)
  - Paginação
  - Glass dark mode

#### 2.9 Frontend — Transaction List Template (melhorada)

- [ ] **Implementar** filtros na `admin_panel/transaction_list.html`:
  - Filtro por tipo, data início, data fim, usuário (select)
  - Botão excluir por transação (com confirmação)
  - Exibir coluna "Usuário"
  - Paginação

#### 2.10 Frontend — Category CRUD Templates

- [ ] **Implementar** templates:
  - `admin_panel/category_list.html` — lista com botões editar/excluir
  - `admin_panel/category_form.html` — form de criação/edição
  - `admin_panel/category_confirm_delete.html` — confirmação de exclusão

#### 2.11 Frontend — Sidebar Admin Link (`core/templates/base.html`)

- [ ] **Implementar** item "Admin" no sidebar condicional:
  - `{% if user.is_staff %}` bloco com link para `admin_panel:dashboard`
  - Ícone shield/settings SVG
  - Highlight ativo quando `request.resolver_match.namespace == 'admin_panel'`
  - Posicionar após os itens de navegação principal (antes do logout)

#### 2.12 Testes E2E (Feature 2)

- [ ] **Ler skill `testing-workflow`**
- [ ] Testes unitários/integração `pytest` passando
- [ ] _(Opcional)_ Teste E2E Playwright: staff acessa admin, vê KPIs, navega subpáginas

#### 2.13 Commit (Feature 2)

- [ ] **Ler skill `git-workflow`**
- [ ] Commit: `feat(admin_panel): add full admin dashboard with users, transactions, categories`

---

### Finais

- [ ] `requirements/requirements.txt` atualizado (se novos pacotes necessários — `ofxparse`, `pdfplumber`)
- [ ] README Curator invocado — atualizar README com novas features
- [ ] Todos os testes passando (`pytest`)
- [ ] Sem itens bloqueados

---

## Riscos e Premissas

| # | Tipo | Descrição |
|---|------|-----------|
| R1 | Risco | `ofxparse` e `pdfplumber` podem não estar no `requirements.txt` — verificar e adicionar |
| R2 | Risco | Parsers de PDF são heurísticos — podem falhar com formatos bancários desconhecidos |
| R3 | Risco | Toggle de usuário pode desativar admin logado — implementar guard |
| R4 | Premissa | `process_bank_statement_import()` já funciona e está testado (CSV confirmado em tests.py) |
| R5 | Premissa | `StaffRequiredMixin` já existe e funciona (confirmado em admin_panel/views.py) |
| R6 | Premissa | Alpine.js já está carregado no base.html (CDN confirmado) |
| R7 | Premissa | Categorias "globais" do admin são categorias criadas com usuario=staff_user |

---

## Arquivos Impactados

| Arquivo | Feature | Ação |
|---------|---------|------|
| `finances/forms.py` | F1 | Adicionar `ImportStatementForm` |
| `finances/views.py` | F1 | Adicionar `ImportStatementView` |
| `finances/urls.py` | F1 | Adicionar URL `import_statement` |
| `finances/templates/finances/transaction_list.html` | F1 | Botão + modal de importação |
| `finances/tests.py` | F1 | Testes do form e view |
| `admin_panel/selectors.py` | F2 | Criar arquivo com selectors de admin |
| `admin_panel/views.py` | F2 | Novas views (dashboard, users, categories) |
| `admin_panel/urls.py` | F2 | Novas URLs |
| `admin_panel/templates/admin_panel/dashboard.html` | F2 | Refatorar com KPIs |
| `admin_panel/templates/admin_panel/user_list.html` | F2 | Criar template |
| `admin_panel/templates/admin_panel/transaction_list.html` | F2 | Melhorar com filtros |
| `admin_panel/templates/admin_panel/category_list.html` | F2 | Criar template |
| `admin_panel/templates/admin_panel/category_form.html` | F2 | Criar template |
| `admin_panel/templates/admin_panel/category_confirm_delete.html` | F2 | Criar template |
| `admin_panel/tests.py` | F2 | Testes de selectors, views, permissões |
| `core/templates/base.html` | F2 | Link Admin no sidebar |
| `requirements/requirements.txt` | Ambas | Verificar `ofxparse`, `pdfplumber` |

---

## Log de Progresso

- 2026-03-25: Plano criado com análise do código existente. Backend de importação (`process_bank_statement_import`, parsers, `_auto_categorize`) já funciona e está testado. Admin panel atual tem apenas dashboard vazio e listagem simples.

---

## Validação Final

- [ ] Todos os itens do checklist marcados
- [ ] Testes passando (`pytest`)
- [ ] README atualizado
- [ ] Sem itens bloqueados
