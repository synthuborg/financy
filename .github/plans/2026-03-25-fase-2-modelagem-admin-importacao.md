# Plano: Fase 2 — Modelagem, Admin Panel e Motor de Importação

**Data:** 2026-03-25
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Implementar os modelos de dados definitivos (`Category`, `Transaction`, `Account`), um painel administrativo protegido com CBVs, e um motor de importação de extratos bancários (CSV, OFX, PDF) com auto-categorização baseada em keywords.

---

## Escopo

### Incluido
- Model `Category` com campos `nome`, `tipo` (entrada/saída), FK `usuario`, `keywords` (CSV para auto-categorização)
- Model `Transaction` com campos `valor`, `data`, `tipo`, `descricao`, FK `categoria`, FK `usuario`
- Model `Account` com campos `nome`, `tipo` (conta_corrente/carteira/cartao_credito), FK `usuario` — relacionado com `Transaction` (null=True temporariamente)
- Validação de banco: `valor > 0` via `CheckConstraint`
- NÃO registrar nenhum model no `admin.py` padrão do Django
- Novo app `admin_panel` com `AdminDashboardView` e `AdminTransactionListView` (CBVs)
- Proteção via `UserPassesTestMixin` (apenas `is_staff=True`)
- URLs do `admin_panel` protegidas e registradas no roteador principal
- Função `process_bank_statement_import(file, user, account)` em `finances/services.py`
- Suporte a CSV, OFX (`ofxparse`) e PDF (`pdfplumber`)
- Auto-categorização cruzando `descricao` da transação com `keywords` das categorias do usuário
- Fallback para categoria `"Avulsa"` (criada automaticamente se não existir)
- Libs adicionadas ao `requirements/requirements.txt`: `ofxparse`, `pdfplumber`

### Fora de escopo
- CRUD de usuários no `admin_panel` (escopo futuro)
- Interface frontend para importação de extratos (coberta na Fase 3+)
- Recuperação de senha, OAuth, perfil de usuário
- Deploy, Docker, banco de dados de produção
- Registros no admin padrão do Django (`/admin/`)

---

## Checklist de Execução

### Pré-requisitos
- [ ] Ler skill `django-patterns` (`.github/skills/django-patterns/SKILL.md`)
- [ ] Ler skill `testing-workflow` (`.github/skills/testing-workflow/SKILL.md`)
- [ ] Instalar libs: `pip install ofxparse pdfplumber`
- [ ] Adicionar `ofxparse` e `pdfplumber` em `requirements/requirements.txt`

---

### Backend — Modelos (`finances/models.py`)

#### Skill: `django-patterns`
- [ ] Revisar SKILL antes de escrever qualquer model

#### 1. Model `Category`
- [ ] **[RED]** Escrever testes:
  - Criação com campos obrigatórios (`nome`, `tipo`, `usuario`)
  - `__str__` retorna `"{tipo} — {nome}"`
  - `tipo` aceita apenas `"entrada"` ou `"saida"` (choices)
  - Campo `keywords` é opcional (blank=True, default `""`)
- [ ] **[GREEN]** Implementar `Category` em `finances/models.py`:
  - `nome`: `CharField(max_length=100)`
  - `tipo`: `CharField(max_length=10, choices=[("entrada","Entrada"),("saida","Saída")])`
  - `keywords`: `TextField(blank=True, default="")`
  - `usuario`: `ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)`
  - `__str__`: `f"{self.get_tipo_display()} — {self.nome}"`
- [ ] Executar testes do model `Category` — confirmar GREEN

#### 2. Model `Transaction`
- [ ] **[RED]** Escrever testes:
  - Criação com campos obrigatórios (`valor`, `data`, `tipo`, `usuario`)
  - `__str__` retorna `"{tipo} R${valor} em {data}"`
  - `CheckConstraint` impede `valor <= 0` a nível de banco
  - FK `categoria` aceita null (`null=True, blank=True`)
  - FK `account` aceita null (`null=True, blank=True`)
- [ ] **[GREEN]** Implementar `Transaction` em `finances/models.py`:
  - `valor`: `DecimalField(max_digits=12, decimal_places=2)`
  - `data`: `DateField()`
  - `tipo`: `CharField(max_length=10, choices=[("entrada","Entrada"),("saida","Saída")])`
  - `descricao`: `TextField(blank=True, default="")`
  - `categoria`: `ForeignKey(Category, on_delete=SET_NULL, null=True, blank=True)`
  - `account`: `ForeignKey("Account", on_delete=SET_NULL, null=True, blank=True)`
  - `usuario`: `ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)`
  - `Meta.constraints`: `CheckConstraint(check=Q(valor__gt=0), name="transaction_valor_positivo")`
  - `__str__`: `f"{self.get_tipo_display()} R${self.valor} em {self.data}"`
- [ ] Executar testes do model `Transaction` — confirmar GREEN

#### 3. Model `Account`
- [ ] **[RED]** Escrever testes:
  - Criação com campos obrigatórios (`nome`, `tipo`, `usuario`)
  - `__str__` retorna `"{nome} ({tipo})"`
  - `tipo` aceita apenas `"conta_corrente"`, `"carteira"` ou `"cartao_credito"` (choices)
- [ ] **[GREEN]** Implementar `Account` em `finances/models.py`:
  - `nome`: `CharField(max_length=100)`
  - `tipo`: `CharField(max_length=20, choices=[("conta_corrente","Conta Corrente"),("carteira","Carteira"),("cartao_credito","Cartão de Crédito")])`
  - `usuario`: `ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)`
  - `__str__`: `f"{self.nome} ({self.get_tipo_display()})"`
- [ ] Executar testes do model `Account` — confirmar GREEN

#### 4. Migrações
- [ ] Rodar `python manage.py makemigrations finances`
- [ ] Rodar `python manage.py migrate`
- [ ] Confirmar que nenhum model está registrado em `finances/admin.py`

#### Code Review — Modelos
- [ ] Ler skill `code-review` (`.github/skills/code-review/SKILL.md`)
- [ ] Verificar: sem imports não utilizados
- [ ] Verificar: PEP8, terminologia correta ("Entrada"/"Saída")
- [ ] Verificar: `admin.py` de `finances` vazio ou com apenas `pass`

---

### Backend — App `admin_panel`

#### 1. Criação do App
- [ ] Rodar `python manage.py startapp admin_panel`
- [ ] Adicionar `admin_panel` ao `INSTALLED_APPS` em `fintrack/settings.py`
- [ ] Criar `admin_panel/services.py` e `admin_panel/selectors.py` (placeholders)

#### 2. CBVs Protegidas
- [ ] **[RED]** Escrever testes de integração:
  - Usuário anônimo recebe **302** ao acessar `GET /admin-panel/`
  - Usuário comum (`is_staff=False`) recebe **403** ao acessar `GET /admin-panel/`
  - Usuário staff (`is_staff=True`) recebe **200** ao acessar `GET /admin-panel/`
  - Usuário anônimo recebe **302** ao acessar `GET /admin-panel/transacoes/`
  - Usuário comum recebe **403** ao acessar `GET /admin-panel/transacoes/`
  - Usuário staff recebe **200** ao acessar `GET /admin-panel/transacoes/`
- [ ] **[GREEN]** Implementar mixin de proteção em `admin_panel/views.py`:
  ```python
  class StaffRequiredMixin(UserPassesTestMixin):
      def test_func(self):
          return self.request.user.is_staff
  ```
- [ ] **[GREEN]** Implementar `AdminDashboardView(StaffRequiredMixin, TemplateView)`:
  - Template: `admin_panel/dashboard.html`
  - Contexto: contagem de usuários, transações totais, categorias
- [ ] **[GREEN]** Implementar `AdminTransactionListView(StaffRequiredMixin, ListView)`:
  - Model: `Transaction`
  - `queryset`: todas as transações (sem filtro por usuário)
  - `ordering`: `["-data"]`
  - Template: `admin_panel/transaction_list.html`
- [ ] Criar templates stub: `admin_panel/templates/admin_panel/dashboard.html` e `transaction_list.html`
- [ ] Configurar `admin_panel/urls.py` com `app_name = "admin_panel"`
- [ ] Incluir `admin_panel.urls` em `fintrack/urls.py` com prefixo `admin-panel/`
- [ ] Executar testes de integração — confirmar GREEN

#### Code Review — admin_panel
- [ ] Verificar: `raise_exception = True` no mixin para retornar 403 (não redirecionar) ao autenticado sem permissão
- [ ] Verificar: sem lógica de negócio nas views
- [ ] Verificar: PEP8

---

### Backend — Motor de Importação (`finances/services.py`)

#### 1. Função Principal
- [ ] **[RED]** Escrever testes unitários para `process_bank_statement_import`:
  - **CSV**: parsing correto de arquivo CSV mínimo (3 colunas: data, descrição, valor)
  - **OFX**: parsing correto via `ofxparse`
  - **PDF**: parsing correto via `pdfplumber` (mock do texto extraído)
  - **Auto-categorização**: transação com descrição contendo keyword de categoria → categoria associada corretamente
  - **Fallback "Avulsa"**: transação sem match de keyword → categoria "Avulsa" criada/atribuída
  - **Fallback criação**: categoria "Avulsa" não existia → é criada automaticamente no banco
  - **Retorno**: função retorna lista de `Transaction` criadas
- [ ] **[GREEN]** Implementar `process_bank_statement_import(file, user, account)` em `finances/services.py`:
  ```python
  def process_bank_statement_import(file, user, account):
      ...
  ```
  - Detectar formato pelo `file.name` (extensão `.csv`, `.ofx`, `.pdf`)
  - Parsear transactions brutas em lista de dicts `{data, descricao, valor, tipo}`
  - Para cada transação bruta:
    1. Cruzar `descricao.lower()` com `keywords` de cada `Category` do usuário
    2. Se match → atribuir categoria; senão → buscar/criar `Category(nome="Avulsa", tipo="saida", usuario=user)`
    3. Criar objeto `Transaction` e salvar no banco
  - Retornar lista de `Transaction` criadas

#### 2. Parsers Internos (funções privadas)
- [ ] **[GREEN]** `_parse_csv(file) -> list[dict]`
- [ ] **[GREEN]** `_parse_ofx(file) -> list[dict]`
- [ ] **[GREEN]** `_parse_pdf(file) -> list[dict]`

#### 3. Utilitário de Auto-categorização
- [ ] **[GREEN]** `_auto_categorize(descricao: str, categorias: QuerySet) -> Category | None`
  - Itera sobre categorias, split de `keywords` por vírgula
  - Retorna primeira categoria cujo keyword estiver contido em `descricao.lower()`
  - Retorna `None` se nenhuma categoria tiver match

#### Code Review — services.py
- [ ] Verificar: funções privadas com prefixo `_`
- [ ] Verificar: sem lógica de view nas funções de serviço
- [ ] Verificar: `ofxparse` e `pdfplumber` importados apenas no topo do arquivo, não dentro de funções
- [ ] Verificar: ausência de vulnerabilidades de injeção no parsing de arquivos

---

### Testes

#### Skill: `testing-workflow` + `playwright-automation`
- [ ] Ler `.github/skills/testing-workflow/SKILL.md`

#### Unitários — Modelos
- [ ] `Category`: criação, `__str__`, choices, campo `keywords` opcional
- [ ] `Transaction`: criação, `__str__`, `CheckConstraint` (valor > 0), FKs nullable
- [ ] `Account`: criação, `__str__`, choices de tipo

#### Integração — admin_panel
- [ ] Usuário anônimo → 302 em `GET /admin-panel/`
- [ ] Usuário comum (`is_staff=False`) → 403 em `GET /admin-panel/`
- [ ] Usuário staff (`is_staff=True`) → 200 em `GET /admin-panel/`
- [ ] Mesmos três cenários para `GET /admin-panel/transacoes/`

#### Unitários — Motor de Importação
- [ ] CSV com 3 linhas → retorna 3 `Transaction` no banco
- [ ] OFX mínimo → transações criadas corretamente
- [ ] PDF com texto mockado → transações criadas corretamente
- [ ] Keyword match → categoria correta associada
- [ ] Sem keyword match → categoria "Avulsa" associada
- [ ] "Avulsa" não existe → criada automaticamente antes de associar

#### Execução Final
- [ ] `pytest --tb=short` — zero falhas
- [ ] Cobertura: `pytest --cov=finances --cov=admin_panel --cov-report=term-missing`

---

### Dependencies
- [ ] `ofxparse` adicionado em `requirements/requirements.txt`
- [ ] `pdfplumber` adicionado em `requirements/requirements.txt`
- [ ] `pip install ofxparse pdfplumber` executado no ambiente local

---

### Git
- [ ] Ler skill `git-workflow` (`.github/skills/git-workflow/SKILL.md`)
- [ ] Commit dos modelos: `feat(finances): add Category, Transaction, Account models with constraints`
- [ ] Commit do admin_panel: `feat(admin_panel): add AdminDashboardView and AdminTransactionListView with staff protection`
- [ ] Commit do motor de importação: `feat(finances): add process_bank_statement_import with CSV/OFX/PDF support and auto-categorization`
- [ ] Commit dos testes: `test(finances/admin_panel): add unit and integration tests for phase 2`
- [ ] Commit das dependências: `chore(requirements): add ofxparse and pdfplumber`

---

## Riscos e Premissas
- **Risco**: parsing de PDF bancário é altamente variável entre bancos — testes devem usar texto mockado genérico
- **Risco**: `CheckConstraint` de banco pode não ser verificado em testes SQLite sem `full_clean()` — usar `pytest.raises(IntegrityError)` com `transaction.atomic()`
- **Premissa**: app `finances` já existe com `selectors.py` e `services.py`
- **Premissa**: `AUTH_USER_MODEL` usa o `User` padrão do Django (`django.contrib.auth`)
- **Premissa**: `admin_panel` NÃO substitui o `/admin/` nativo do Django
- **Premissa**: `raise_exception = True` no `UserPassesTestMixin` é obrigatório para garantir HTTP 403 (não redirect) para usuários autenticados sem `is_staff`

---

## Log de Progresso
- 2026-03-25: Plano criado pelo Planner Checklist — Fase 2 iniciada

---

## Definição de Pronto (DoD)
- [ ] Todos os itens do checklist marcados com `[x]`
- [ ] `pytest` — zero falhas, cobertura ≥ 80% nos apps `finances` e `admin_panel`
- [ ] Nenhum model registrado no `admin.py` padrão do Django
- [ ] `UserPassesTestMixin` retornando HTTP 403 (não 302) para usuários autenticados sem `is_staff`
- [ ] `ofxparse` e `pdfplumber` em `requirements/requirements.txt`
- [ ] Categoria "Avulsa" criada automaticamente por `get_or_create` (sem duplicatas)
- [ ] Commits separados por domínio conforme checklist Git
- [ ] Sem violações PEP8 detectadas pelo `code-review`
