# FinTrack

> Aplicação de controle financeiro pessoal para registro e visualização de entradas e saídas, com dashboard analítico interativo.

**Equipe:** JRD Labs · **Evento:** Hackathon

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Django](https://img.shields.io/badge/Django-5.x-green)
![Testes](https://img.shields.io/badge/testes-151%20passando-brightgreen)
![Status](https://img.shields.io/badge/fase%201-conclu%C3%ADda-success)
![Status](https://img.shields.io/badge/fase%201.5-conclu%C3%ADda-success)
![Status](https://img.shields.io/badge/fase%202-conclu%C3%ADda-success)
![Status](https://img.shields.io/badge/fase%203-conclu%C3%ADda-success)
![Status](https://img.shields.io/badge/fase%204-conclu%C3%ADda-success)
![Status](https://img.shields.io/badge/fase%205-conclu%C3%ADda-success)
![Status](https://img.shields.io/badge/fase%206-conclu%C3%ADda-success)
![Status](https://img.shields.io/badge/fase%207-conclu%C3%ADda-success)

---

## Funcionalidades

- Cadastro de categorias por tipo (entrada / saída)
- Registro de transações com valor, data, descrição e categoria
- Landing page com hero section, cards de features e CTA
- Cadastro e login de usuários com formulários estilizados
- Dashboard com 4 gráficos carregados de forma assíncrona via HTMX
- Evolução de entradas e saídas nos últimos 6 meses
- Distribuição de saídas por categoria no mês atual
- KPIs do mês corrente: Entradas, Saídas e Saldo Líquido em cards coloridos
- Atividade recente: últimas 5 transações com tipo colorido por ícone
- Sidebar global de navegação (Dashboard, Transações, Categorias, Contas Correntes, Cartões, Metas, Relatórios)
- Filtros GET na lista de transações: tipo, data inicial, data final e busca por descrição
- Autenticação com sistema nativo do Django (`contrib.auth`)
- Gerenciamento de contas com telas separadas para Contas Correntes/Carteiras e Cartões de Crédito
- Cards de contas correntes exibem saldo e as últimas 5 transações com cor indicativa (verde para entradas, vermelho para saídas)
- Formatação monetária brasileira (R$ 1.234,56) com separador de milhares em todas as telas
- Telas de login e registro standalone com design glass (sem sidebar)
- Cadastro e monitoramento de metas financeiras com barra de progresso e depósito inline
- Top 3 metas exibidas no dashboard com barras de progresso coloridas
- Motor de importação de extratos bancários (CSV, OFX, PDF) com auto-categorização por palavras-chave
- Gerador de relatórios financeiros em PDF (ReportLab) e Excel (OpenPyXL) com filtro por período
- Admin Panel protegido por perfil staff (`/admin-panel/`)
- Integração Telegram multitenant por usuário (`/telegram/configurar/`) com onboarding para validar token, detectar chat_id e registrar webhook
- Registro de transações em linguagem natural via bot Telegram (ex.: "gastei 50 no mercado", "recebi 3000 de salário")
- Atualização automática da atividade recente no dashboard e da listagem de transações via websocket/OOB (sem polling contínuo)
- Orçamento mensal por percentual da renda com limite diário dinâmico, calendário de gastos, alertas no dashboard e notificações no Telegram (20%, 10%, 100% e pós-limite)

---

## Tecnologias

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.11+ | Linguagem base |
| Django | 5.2 | Framework web |
| SQLite | — | Banco de dados (desenvolvimento) |
| Tailwind CSS | CDN | Estilização dark mode |
| Alpine.js | CDN | Navbar adaptativa (glass ao scroll) |
| HTMX | CDN | Lazy loading dos gráficos |
| ApexCharts | CDN | Visualizações dos gráficos |
| pytest-django | 4.7+ | Suite de testes |
| ofxparse | 0.21 | Leitura de extratos OFX |
| pdfplumber | 0.11.9 | Extração de texto de PDFs |
| reportlab | 4.4.10 | Geração de relatórios em PDF |
| openpyxl | 3.1.5 | Geração de relatórios em Excel |

Dependências completas: [`requirements/requirements.txt`](requirements/requirements.txt)

---

## Pré-requisitos

- Python 3.11+
- pip
- virtualenv (ou `python -m venv`)

---

## Como Rodar

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd smartfinancy

# 2. Criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements/requirements.txt

# 4. Aplicar migrações
python manage.py migrate

# 5. Criar superusuário
python manage.py createsuperuser

# 6. Iniciar servidor
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/ (landing page)
Ou diretamente: http://127.0.0.1:8000/dashboard/

---

## Rotas

| Rota | View | Descrição |
|---|---|---|
| `GET /` | `LandingPageView` | Landing page pública |
| `GET /accounts/login/` | `CustomLoginView` | Tela de login |
| `POST /accounts/login/` | `CustomLoginView` | Autenticar usuário |
| `GET /accounts/register/` | `RegisterView` | Tela de cadastro |
| `POST /accounts/register/` | `RegisterView` | Criar novo usuário |
| `POST /accounts/logout/` | `CustomLogoutView` | Encerrar sessão |
| `GET /dashboard/` | `DashboardView` | Dashboard principal (autenticado) |
| `GET /dashboard/htmx/grafico-evolucao/` | — | Fragmento: evolução 6 meses |
| `GET /dashboard/htmx/grafico-saidas/` | — | Fragmento: distribuição de saídas |
| `GET /dashboard/htmx/grafico-metas/` | — | Fragmento: progresso de metas |
| `GET /dashboard/htmx/grafico-investimentos/` | — | Fragmento: carteira de investimentos |
| `GET /telegram/configurar/` | `TelegramConfigView` | Onboarding e status da integração Telegram |
| `POST /telegram/api/validate-token/` | `api_validate_token` | Valida token do bot no Telegram |
| `POST /telegram/api/detect-chat-id/` | `api_detect_chat_id` | Detecta chat_id por `getUpdates` |
| `POST /telegram/api/save-config/` | `api_save_config` | Salva credenciais (hash + cifrado), registra comandos e webhook |
| `POST /telegram/api/disconnect/` | `api_disconnect` | Remove configuração do usuário e webhook |
| `POST /telegram/webhook/` | `telegram_webhook` | Processa mensagens do Telegram e cria transações |
| `GET /telegram/htmx/dashboard-parcial/` | `dashboard_partial` | Fragmento HTMX com atividade recente e resumo |
| `GET /admin-panel/` | `AdminDashboardView` | Painel administrativo (apenas staff) |
| `GET /admin-panel/transacoes/` | `AdminTransactionListView` | Lista de transações — admin (apenas staff) |
| `GET /financas/transacoes/` | `TransactionListView` | Lista de transações do usuário |
| `GET /financas/transacoes/nova/` | `TransactionCreateView` | Formulário de criação de transação |
| `POST /financas/transacoes/nova/` | `TransactionCreateView` | Criar transação |
| `GET /financas/transacoes/<pk>/editar/` | `TransactionUpdateView` | Formulário de edição de transação |
| `POST /financas/transacoes/<pk>/editar/` | `TransactionUpdateView` | Atualizar transação |
| `GET /financas/transacoes/<pk>/excluir/` | `TransactionDeleteView` | Confirmação de exclusão |
| `POST /financas/transacoes/<pk>/excluir/` | `TransactionDeleteView` | Excluir transação |
| `GET /financas/categorias/` | `CategoryListView` | Lista de categorias do usuário |
| `GET /financas/categorias/nova/` | `CategoryCreateView` | Formulário de criação de categoria |
| `POST /financas/categorias/nova/` | `CategoryCreateView` | Criar categoria |
| `GET /financas/categorias/<pk>/editar/` | `CategoryUpdateView` | Formulário de edição de categoria |
| `POST /financas/categorias/<pk>/editar/` | `CategoryUpdateView` | Atualizar categoria |
| `GET /financas/categorias/<pk>/excluir/` | `CategoryDeleteView` | Confirmação de exclusão de categoria |
| `POST /financas/categorias/<pk>/excluir/` | `CategoryDeleteView` | Excluir categoria |
| `GET /financas/contas/` | `AccountListView` | Lista de contas do usuário |
| `GET /financas/contas/nova/` | `AccountCreateView` | Formulário de criação de conta |
| `POST /financas/contas/nova/` | `AccountCreateView` | Criar conta |
| `GET /financas/contas/<pk>/editar/` | `AccountUpdateView` | Formulário de edição de conta |
| `POST /financas/contas/<pk>/editar/` | `AccountUpdateView` | Atualizar conta |
| `GET /financas/contas/<pk>/excluir/` | `AccountDeleteView` | Confirmação de exclusão de conta |
| `POST /financas/contas/<pk>/excluir/` | `AccountDeleteView` | Excluir conta |
| `GET /financas/conta-corrente/` | `ContaCorrenteListView` | Lista de contas correntes com saldo e transações recentes |
| `GET /financas/conta-corrente/nova/` | `ContaCorrenteCreateView` | Formulário de criação de conta corrente |
| `POST /financas/conta-corrente/nova/` | `ContaCorrenteCreateView` | Criar conta corrente |
| `GET /financas/conta-corrente/<pk>/editar/` | `ContaCorrenteUpdateView` | Formulário de edição de conta corrente |
| `POST /financas/conta-corrente/<pk>/editar/` | `ContaCorrenteUpdateView` | Atualizar conta corrente |
| `GET /financas/conta-corrente/<pk>/excluir/` | `ContaCorrenteDeleteView` | Confirmação de exclusão de conta corrente |
| `POST /financas/conta-corrente/<pk>/excluir/` | `ContaCorrenteDeleteView` | Excluir conta corrente |
| `GET /financas/cartao/` | `CartaoCreditoListView` | Lista de cartões de crédito |
| `GET /financas/cartao/novo/` | `CartaoCreditoCreateView` | Formulário de criação de cartão |
| `POST /financas/cartao/novo/` | `CartaoCreditoCreateView` | Criar cartão de crédito |
| `GET /financas/cartao/<pk>/editar/` | `CartaoCreditoUpdateView` | Formulário de edição de cartão |
| `POST /financas/cartao/<pk>/editar/` | `CartaoCreditoUpdateView` | Atualizar cartão de crédito |
| `GET /financas/cartao/<pk>/excluir/` | `CartaoCreditoDeleteView` | Confirmação de exclusão de cartão |
| `POST /financas/cartao/<pk>/excluir/` | `CartaoCreditoDeleteView` | Excluir cartão de crédito |
| `GET /financas/metas/` | `GoalListView` | Lista de metas do usuário |
| `GET /financas/metas/nova/` | `GoalCreateView` | Formulário de criação de meta |
| `POST /financas/metas/nova/` | `GoalCreateView` | Criar meta |
| `GET /financas/metas/<pk>/editar/` | `GoalUpdateView` | Formulário de edição de meta |
| `POST /financas/metas/<pk>/editar/` | `GoalUpdateView` | Atualizar meta |
| `GET /financas/metas/<pk>/excluir/` | `GoalDeleteView` | Confirmação de exclusão de meta |
| `POST /financas/metas/<pk>/excluir/` | `GoalDeleteView` | Excluir meta |
| `POST /financas/metas/<pk>/progresso/` | `GoalAddProgressView` | Adicionar progresso a uma meta |
| `GET /financas/orcamento/` | `MonthlyBudgetConfigView` | Configurar orçamento mensal, alertas e acompanhar calendário de gastos |
| `POST /financas/orcamento/` | `MonthlyBudgetConfigView` | Salvar configuração de orçamento e preferências de alerta |
| `GET /financas/relatorios/` | `ReportFormView` | Formulário de geração de relatório |
| `POST /financas/relatorios/` | `ReportFormView` | Gerar relatório em PDF ou Excel |

---

## Landing Page & Autenticação

A landing page usa design **Glassmorphism Premium Dark**: fundo escuro com elementos semitransparentes, blur e gradientes.

---

## Telegram Bot (Segurança)

- Cada usuário possui configuração isolada (`TelegramCredential`) no app separado `telegram_bot`.
- `token` e `chat_id` **não são persistidos em texto puro**.
- O banco armazena `token_hash` e `chat_id_hash` para verificação/lookup.
- O token também é armazenado cifrado (`token_encrypted`) para uso operacional na API do Telegram.
- O webhook identifica o usuário por `chat_id_hash`, sem fallback para outro usuário.

### Variáveis de ambiente opcionais

No arquivo de configuração (`fintrack/settings.py`):

- `TELEGRAM_TOKEN_ENCRYPTION_KEY`: chave Fernet URL-safe base64 (quando não informada, deriva de `SECRET_KEY` em desenvolvimento)
- `TELEGRAM_HASH_SECRET`: segredo para HMAC-SHA256 (quando não informado, usa `SECRET_KEY`)

**Componentes da landing page:**
- Navbar com efeito glass ao rolar a página (gerenciado por Alpine.js)
- Hero section com mockup flutuante exibindo cartões de Entradas e Saídas
- Seção de features com 3 cards glass
- CTA final e footer

**Telas de autenticação:**
- `login.html` e `register.html` com páginas standalone (sem sidebar) e formulários estilizados no padrão glass
- Redirecionamento pós-login para `/dashboard/` e pós-logout para `/`

**Classes CSS do tema:**

```css
.glass            /* card semitransparente com backdrop-blur */
.gradient-text    /* texto com gradiente verde-azul */
.animate-float    /* animação de flutuação suave */
```

---

## Fluxo de Dados

O projeto adota separação estrita de responsabilidades dentro de cada app Django:

```
Request
   │
   ▼
views.py        ← orquestra request/response, sem lógica de negócio
   │
   ├──▶ services.py   ← operações CUD (Create, Update, Delete)
   │                     regras de negócio e validações
   │
   └──▶ selectors.py  ← consultas otimizadas (Read-only)
              │
              ▼
          models.py   ← definição dos dados (Category, Transaction, Account, Goal)
```

| Camada | Responsabilidade |
|---|---|
| **View** | Orquestra request/response; sem lógica de negócio |
| **Service** | Regras de negócio (CUD), validações, exceções |
| **Selector** | Consultas otimizadas (Read), evita N+1 com `select_related` |
| **Model** | Persistência, constraints de banco, validações de schema |

**Regra:** nenhuma query complexa em `views.py`. Views chamam apenas `services` e `selectors`.

---

## Dashboard — HTMX Lazy Loading

Cada gráfico do dashboard é carregado de forma independente e assíncrona. A página principal entrega a estrutura imediatamente; cada card dispara sua própria requisição HTMX ao ser renderizado.

```html
<!-- Exemplo de card com lazy loading -->
<div hx-get="/dashboard/htmx/grafico-evolucao/"
     hx-trigger="load"
     hx-swap="innerHTML">
  <!-- spinner exibido enquanto carrega -->
</div>
```

**Rotas HTMX disponíveis:**

| Rota | Gráfico |
|---|---|
| `GET /dashboard/htmx/grafico-evolucao/` | Evolução de entradas e saídas (6 meses) |
| `GET /dashboard/htmx/grafico-saidas/` | Distribuição de saídas por categoria |
| `GET /dashboard/htmx/grafico-metas/` | Progresso de metas (top 3 do usuário) |
| `GET /dashboard/htmx/grafico-investimentos/` | Carteira de investimentos (dados mockados) |

---

## Dashboard — KPIs e Atividade Recente

Além dos gráficos HTMX, o dashboard exibe dados síncronos calculados em `dashboard/selectors.py`:

**Cards KPI (mês corrente):**

| Card | Cor | Dado |
|---|---|---|
| Entradas do mês | Emerald | Soma das entradas do mês atual |
| Saídas do mês | Vermelho | Soma das saídas do mês atual |
| Saldo Líquido | Violet (positivo) / Vermelho (negativo) | Entradas − Saídas |

**Atividade Recente:**

Tabela com as últimas 5 transações do usuário, exibindo descrição, data, categoria e valor com ícone colorido por tipo (↑ emerald para Entradas, ↓ vermelho para Saídas).

**Seletores envolvidos:**

- `obter_resumo_mes_atual(user)` — totais do mês corrente agrupados por tipo
- `obter_ultimas_transacoes(user, limit=5)` — últimas N transações ordenadas por data

---

## Filtros de Transações

A rota `GET /financas/transacoes/` aceita os seguintes parâmetros de query string:

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `tipo` | `entrada` \| `saida` | Filtra transações pelo tipo |
| `data_inicio` | `YYYY-MM-DD` | Retorna transações a partir desta data |
| `data_fim` | `YYYY-MM-DD` | Retorna transações até esta data |
| `q` | texto | Busca por descrição (case-insensitive, contém) |

Exemplo:

```
/financas/transacoes/?tipo=saida&data_inicio=2026-03-01&q=mercado
```

Os filtros são combinados (AND). Sem parâmetros, retorna todas as transações do usuário.

---

## Estrutura do Projeto

```
smartfinancy/
├── manage.py
├── conftest.py
├── pytest.ini
├── requirements/
│   └── requirements.txt
├── fintrack/               # configurações do projeto Django
│   ├── settings.py
│   └── urls.py
├── accounts/               # cadastro e autenticação de usuários
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── accounts/
│           ├── login.html
│           └── register.html
├── core/                   # landing page e template base
│   ├── models.py
│   ├── views.py
│   └── templates/
│       ├── base.html
│       └── core/
│           └── landing_page.html
├── finances/               # CRUD de transações, categorias, contas e metas
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── services.py
│   ├── selectors.py
│   ├── migrations/
│   └── templates/
│       └── finances/
│           ├── report_form.html
│           ├── transaction_list.html
│           ├── transaction_form.html
│           ├── transaction_confirm_delete.html
│           ├── category_list.html
│           ├── category_form.html
│           ├── category_confirm_delete.html
│           ├── account_list.html
│           ├── account_form.html
│           ├── account_confirm_delete.html
│           ├── goal_list.html
│           ├── goal_form.html
│           └── goal_confirm_delete.html
├── admin_panel/            # painel administrativo (apenas staff)
│   ├── views.py
│   └── templates/
│       └── admin_panel/
│           ├── dashboard.html
│           └── transaction_list.html
└── dashboard/              # views e gráficos do dashboard
    ├── views.py
    ├── services.py
    ├── selectors.py
    ├── urls.py
    └── templates/
        └── dashboard/
            ├── dashboard.html
            └── fragmentos/
                ├── grafico_evolucao.html
                ├── grafico_saidas.html
                ├── grafico_metas.html
                └── grafico_investimentos.html
```

---

## Executar Testes

```bash
# Rodar todos os testes
pytest

# Com saída detalhada
pytest -v

# Com cobertura (se pytest-cov instalado)
pytest --cov
```

Suite atual: **151 testes passando**.

---

## Terminologia

| Termo usado | Evitar | Significado |
|---|---|---|
| **Entrada** | ~~Receita~~ | Dinheiro que entra (salário, freelance, etc.) |
| **Saída** | ~~Despesa~~, ~~Gasto~~ | Dinheiro que sai (contas, compras, etc.) |
| **Transação** | — | Registro de uma entrada ou saída |
| **Categoria** | — | Classificação de uma transação |
| **Conta** | ~~Carteira~~, ~~Banco~~ | Conta Corrente, Carteira ou Cartão de Crédito |
| **Meta** | ~~Objetivo~~, ~~Goal~~ | Objetivo financeiro com valor-alvo e progresso |

---

## Fase 1 — Status

✅ **Concluída**

- [x] Models `Category` e `Transaction` com validações
- [x] Arquitetura limpa: `views` → `services` / `selectors` → `models`
- [x] App `dashboard` com 4 gráficos via ApexCharts
- [x] HTMX lazy loading — cada gráfico carrega de forma independente
- [x] Loading spinner por card durante carregamento
- [x] Autenticação via `django.contrib.auth`

---

## Motor de Importação

O serviço `finances/services.py` (`process_bank_statement_import`) processa extratos bancários enviados pelo usuário.

**Formatos suportados:** CSV, OFX, PDF

**Auto-categorização:**
1. Cada `Category` possui uma lista de palavras-chave (`get_keywords_list()`).
2. A descrição de cada transação importada é comparada com as palavras-chave das categorias do usuário.
3. A primeira categoria com match é aplicada automaticamente.
4. Sem nenhum match, a transação recebe a categoria **"Avulsa"**, criada automaticamente se ainda não existir.

---

## Gerador de Relatórios

A rota `GET /financas/relatorios/` exibe um formulário para geração de relatórios financeiros com filtro por período e formato de saída.

**Formatos disponíveis:** PDF, Excel (`.xlsx`)

**Conteúdo do relatório:**
- Resumo financeiro: total de receitas, despesas e saldo do período
- Transações agrupadas por categoria com subtotais
- Lista detalhada de todas as transações no intervalo selecionado

**PDF (ReportLab):** layout profissional com cabeçalhos, cores e tabelas formatadas.

**Excel (OpenPyXL):** planilha com 3 abas — *Resumo*, *Transações* e *Por Categoria* — com cabeçalhos formatados e colunas auto-dimensionadas.

---

## Fase 1.5 — Status

✅ **Concluída**

- [x] Landing page pública (`/`) com design Glassmorphism Premium Dark
- [x] App `accounts`: `RegisterView`, `CustomLoginView`, `CustomLogoutView`
- [x] Rotas `/accounts/login/`, `/accounts/logout/`, `/accounts/register/`
- [x] Alpine.js para navbar adaptativa (efeito glass ao scroll)
- [x] Telas de autenticação estilizadas (`login.html`, `register.html`)
- [x] `LOGIN_REDIRECT_URL = '/dashboard/'`, `LOGOUT_REDIRECT_URL = '/'`
- [x] 31 testes passando (16 adicionados: 6 landing page + 10 accounts)

---

## Fase 2 — Status

✅ **Concluída**

- [x] Model `Account`: Conta Corrente, Carteira e Cartão de Crédito (FK usuário)
- [x] `Category.get_keywords_list()`: método auxiliar para auto-categorização
- [x] `Transaction.conta`: FK para `Account` (null=True)
- [x] `CheckConstraint` em `Transaction` garantindo valor > 0
- [x] App `admin_panel` com `AdminDashboardView` e `AdminTransactionListView`
- [x] Proteção via `StaffRequiredMixin` — acesso restrito a `is_staff=True`
- [x] Rotas `/admin-panel/` e `/admin-panel/transacoes/`
- [x] `process_bank_statement_import` em `finances/services.py`
- [x] Importação de extratos CSV, OFX e PDF
- [x] Auto-categorização por palavras-chave com fallback "Avulsa"
- [x] 51 testes passando (20 adicionados: 16 finances + 4 admin_panel)

---

## Fase 3 — Status

✅ **Concluída**

- [x] `finances/services.py`: `create_transaction(user, data)` — validação de valor > 0, tipo válido, escopo por usuário
- [x] `finances/services.py`: `update_transaction(transaction_id, user, data)` — atualização parcial com escopo
- [x] `finances/services.py`: `delete_transaction(transaction_id, user)` — remoção com escopo
- [x] `finances/services.py`: `calculate_balance(user)` — retorna `{total_entradas, total_saidas, saldo_liquido}`
- [x] `finances/selectors.py`: `get_all_transactions(user)` — queryset com `select_related('categoria', 'conta')`
- [x] `finances/selectors.py`: `get_transaction_by_id(transaction_id, user)` — `get_object_or_404` + `select_related`
- [x] 71 testes passando (20 adicionados — unitários, independentes de HTTP)

---

## Fase 4 — Status

✅ **Concluída**

- [x] `finances/forms.py`: `TransactionForm` e `CategoryForm` com classes Tailwind/Zinc e querysets filtrados por usuário
- [x] `finances/views.py`: 8 CBVs — `TransactionListView`, `TransactionCreateView`, `TransactionUpdateView`, `TransactionDeleteView`, `CategoryListView`, `CategoryCreateView`, `CategoryUpdateView`, `CategoryDeleteView`
- [x] `finances/urls.py`: 8 rotas com `app_name = 'finances'`
- [x] Inclusão em `fintrack/urls.py`: `path('financas/', include('finances.urls'))`
- [x] 6 templates mobile-first dark mode em `finances/templates/finances/`
- [x] Ícones por tipo de transação: ↑ emerald para Entradas, ↓ vermelho para Saídas
- [x] Isolamento de dados por usuário — `get_queryset()` filtra por `request.user` (OWASP A01)
- [x] Flash messages com Alpine.js (auto-dismiss em 4s)
- [x] 87 testes passando (+16 de integração HTTP)

---

## Fase 5 — Status

✅ **Concluída**

- [x] `dashboard/selectors.py`: `obter_resumo_mes_atual(user)` — totais do mês corrente por tipo
- [x] `dashboard/selectors.py`: `obter_ultimas_transacoes(user, limit=5)` — últimas N transações
- [x] `dashboard/views.py`: `DashboardView` passa `saldo`, `resumo_mes` e `ultimas_transacoes` ao template
- [x] `dashboard/dashboard.html`: 3 cards KPI (Entradas mês, Saídas mês, Saldo Líquido) + tabela Atividade Recente
- [x] `finances/views.py`: `TransactionListView` com filtros GET (`tipo`, `data_inicio`, `data_fim`, `q`)
- [x] `finances/transaction_list.html`: card de filtros com busca por descrição, tipo e intervalo de datas
- [x] `core/base.html`: sidebar global com links para Dashboard, Transações e Categorias
- [x] 104 testes passando (+17 de integração e unitários)

---

## Fase 6 — Status

✅ **Concluída**

- [x] Model `Goal` em `finances/models.py`: `titulo`, `valor_alvo`, `valor_atual`, `prazo` (nullable), FK `usuario`, FK `categoria`
- [x] Properties `percentual_concluido` (int 0–100) e `saldo_restante` (Decimal) em `Goal`
- [x] Migração `finances/migrations/0003_goal.py` criada e aplicada
- [x] `finances/services.py`: `create_goal`, `update_goal`, `delete_goal`, `add_progress_to_goal`
- [x] `finances/selectors.py`: `get_all_goals(user)`, `get_goal_by_id(goal_id, user)`
- [x] 5 CBVs de metas: `GoalListView`, `GoalCreateView`, `GoalUpdateView`, `GoalDeleteView`, `GoalAddProgressView`
- [x] 5 rotas `/financas/metas/` com formulário inline de depósito por card
- [x] 3 templates de metas: `goal_list.html`, `goal_form.html`, `goal_confirm_delete.html`
- [x] Barra de progresso linear colorida: azul (0–49%), violet (50–99%), emerald (100%)
- [x] 4 CBVs de contas: `AccountListView`, `AccountCreateView`, `AccountUpdateView`, `AccountDeleteView`
- [x] 4 rotas `/financas/contas/` com ícones por tipo (azul, emerald, violet)
- [x] 3 templates de contas: `account_list.html`, `account_form.html`, `account_confirm_delete.html`
- [x] `dashboard/selectors.py`: `obter_metas_resumo(user, limit=3)` — top 3 metas do usuário
- [x] Dashboard: card "Minhas Metas" com top 3 metas e barras de progresso
- [x] `DashboardView`: `ctx['metas']` populado via `obter_metas_resumo`
- [x] `core/base.html`: sidebar atualizada com links para Contas e Metas
- [x] 130 testes passando (+26 novos)

---

## Fase 7 — Status

✅ **Concluída**

- [x] `finances/selectors.py`: `get_account_balance(account_id, user)` — saldo isolado por conta
  - Conta Corrente / Carteira: `sum(entradas) - sum(saídas)`
  - Cartão de Crédito: `sum(saídas)` = fatura atual
- [x] `finances/views.py`: 8 novas CBVs separadas por tipo de conta
  - `ContaCorrenteListView`, `ContaCorrenteCreateView`, `ContaCorrenteUpdateView`, `ContaCorrenteDeleteView`
  - `CartaoCreditoListView`, `CartaoCreditoCreateView`, `CartaoCreditoUpdateView`, `CartaoCreditoDeleteView`
- [x] `finances/urls.py`: 8 novas rotas `/financas/conta-corrente/` e `/financas/cartao/`
- [x] `finances/templates/finances/conta_corrente_list.html`: listagem com saldo (verde positivo / vermelho negativo)
- [x] `finances/templates/finances/cartao_credito_list.html`: listagem com fatura em vermelho
- [x] `core/base.html`: sidebar atualizada com links separados para "Contas Correntes" e "Cartões"
- [x] `.github/plans/2026-03-25-fase-7-conta-corrente-cartao.md`: checklist de planejamento criado
- [x] 151 testes passando (+21 novos: 7 unitários `get_account_balance` + 7 `ContaCorrenteViews` + 7 `CartaoCreditoViews`)
