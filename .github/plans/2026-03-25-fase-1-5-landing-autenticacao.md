# Plano: Fase 1.5 — Landing Page e Autenticação

**Data:** 2026-03-25
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Implementar a landing page pública com design Glassmorphism Premium Dark e o sistema de autenticação (login, logout, registro) usando CBVs nativas do Django, criando o app `accounts` e expondo a URL raiz `/`.

---

## Escopo

### Incluido
- `LandingPageView` no app `core` (TemplateView) com template `core/landing_page.html`
- URL raiz `/` apontando para `LandingPageView`
- Novo app `accounts` com `app_name = 'accounts'`
- CBVs: `LoginView`, `LogoutView` (nativas Django) e `RegisterView` (CreateView + UserCreationForm)
- `LOGIN_REDIRECT_URL = '/dashboard/'` no `settings.py`
- `accounts` adicionado ao `INSTALLED_APPS`
- Design landing: Glassmorphism Premium Dark (Tailwind + Alpine.js)
- Navbar responsiva com Alpine.js (transparente → glass ao rolar)
- Hero Section: grade 2 colunas, orbs decorativos, badge, gradient-text, mockup desktop
- Mockup desktop com "Entradas" (verde) e "Saídas" (vermelho) — **INEGOCIÁVEL**
- Seção Features e CTA final
- Telas Login e Register com design glass

### Fora de escopo
- Recuperação de senha / e-mail de verificação
- OAuth / login social
- Perfil de usuário
- Qualquer lógica de dashboard (coberta na Fase 2+)

---

## Checklist de Execucao

### Backend

#### Skill: `django-patterns`
- [ ] Ler `.github/skills/django-patterns/SKILL.md` antes de implementar

#### 1. app `core` — LandingPageView
- [ ] **RED** — Escrever teste: `GET /` retorna HTTP 200 e usa template `core/landing_page.html`
- [ ] **GREEN** — Criar `LandingPageView` em `core/views.py` (TemplateView)
- [ ] **GREEN** — Criar template stub `core/templates/core/landing_page.html` (extends base)
- [ ] **GREEN** — Registrar URL raiz `/` em `fintrack/urls.py`
- [ ] Executar testes — confirmar GREEN

#### 2. app `accounts`
- [ ] **RED** — Escrever testes:
  - `GET /accounts/login/` retorna HTTP 200
  - `GET /accounts/register/` retorna HTTP 200
  - `POST /accounts/register/` com dados válidos cria usuário e redireciona para `/accounts/login/`
  - `POST /accounts/login/` com credenciais válidas redireciona para `/dashboard/`
- [ ] **GREEN** — Criar app com `python manage.py startapp accounts`
- [ ] **GREEN** — Definir `app_name = 'accounts'` em `accounts/urls.py`
- [ ] **GREEN** — Criar `RegisterView` em `accounts/views.py` (CreateView + UserCreationForm)
- [ ] **GREEN** — Configurar `LoginView` e `LogoutView` (nativas Django) em `accounts/urls.py`
- [ ] **GREEN** — Adicionar `accounts` ao `INSTALLED_APPS` em `fintrack/settings.py`
- [ ] **GREEN** — Adicionar `LOGIN_REDIRECT_URL = '/dashboard/'` em `fintrack/settings.py`
- [ ] **GREEN** — Incluir `accounts.urls` em `fintrack/urls.py` com prefixo `accounts/`
- [ ] Executar todos os testes do backend — confirmar GREEN

#### Skill: `code-review`
- [ ] Ler `.github/skills/code-review/SKILL.md` e revisar código gerado
- [ ] Corrigir eventuais violações (PEP8, imports não usados, dead code)

---

### Frontend

#### Skills: `frontend-finance-design` + `htmx-patterns`
- [ ] Ler `.github/skills/frontend-finance-design/SKILL.md`
- [ ] Ler `.github/skills/htmx-patterns/SKILL.md`

#### 1. Base e estilos globais
- [ ] Configurar `body` com `bg-zinc-950 text-zinc-50` no `base.html`
- [ ] Adicionar classe CSS customizada `.glass` (backdrop-blur, border, bg-white/5)
- [ ] Adicionar classe CSS customizada `.gradient-text` (bg-clip-text, transparent)
- [ ] Adicionar animação CSS `float` (keyframes translateY suave)
- [ ] Garantir Alpine.js carregado no `<head>` do `base.html`

#### 2. Navbar
- [ ] Implementar navbar com `x-data` Alpine.js, detectando scroll (`@scroll.window`)
- [ ] Estado: fundo transparente no topo → `.glass` + blur ao rolar
- [ ] Links: "Início", "Funcionalidades", CTA "Entrar" e "Criar conta"
- [ ] Responsividade: hamburger menu mobile com `x-show` / transição Alpine.js

#### 3. Hero Section
- [ ] Layout grade 2 colunas (texto | mockup) — stack em mobile
- [ ] Orbs decorativos: círculos com gradiente verde e roxo, `blur-3xl`, `opacity-20`
- [ ] Badge animado acima do título (ex.: "✦ Controle Financeiro Inteligente")
- [ ] Título com `.gradient-text` (gradiente verde → azul ou verde → roxo)
- [ ] Subtítulo e dois botões CTA: "Começar Grátis" (primary) e "Ver Demo" (outline)
- [ ] **Mockup desktop** (card dark glass, borda zinc-800):
  - [ ] Linha "Entradas" com ícone, valor em **verde** (`text-emerald-400`) — OBRIGATÓRIO
  - [ ] Linha "Saídas" com ícone, valor em **vermelho** (`text-red-400`) — OBRIGATÓRIO
  - [ ] Mini gráfico ou barra de progresso visual decorativa
  - [ ] Animação `float` aplicada ao card do mockup

#### 4. Seção Features
- [ ] Grade 3 colunas (stack em mobile)
- [ ] Ao menos 3 cards glass com ícone SVG, título e descrição
- [ ] Sugestões: "Controle de Gastos", "Metas Financeiras", "Relatórios Visuais"

#### 5. Seção CTA Final
- [ ] Banner centralizado com gradiente sutil de fundo
- [ ] Título, subtítulo e botão "Criar conta gratuita" → `accounts:register`

#### 6. Tela Login (`accounts/templates/accounts/login.html`)
- [ ] Extend `base.html`, layout centralizado verticalmente
- [ ] Card `.glass` com formulário: username, password, botão "Entrar"
- [ ] Link para página de registro
- [ ] Exibir mensagens de erro do form (`{{ form.errors }}`)

#### 7. Tela Register (`accounts/templates/accounts/register.html`)
- [ ] Extend `base.html`, layout centralizado verticalmente
- [ ] Card `.glass` com UserCreationForm: username, password1, password2, botão "Criar conta"
- [ ] Link para página de login
- [ ] Exibir mensagens de erro do form

#### Validação Frontend
- [ ] Responsividade verificada em 375px, 768px e 1280px
- [ ] Alto contraste e legibilidade no dark mode
- [ ] Sem elementos quebrando na tela mobile

---

### Testes

#### Skill: `testing-workflow`
- [ ] Ler `.github/skills/testing-workflow/SKILL.md`

#### Testes unitários / integração (pytest-django)
- [ ] `GET /` → HTTP 200 ✓
- [ ] `GET /accounts/login/` → HTTP 200 ✓
- [ ] `GET /accounts/register/` → HTTP 200 ✓
- [ ] `POST /accounts/register/` dados válidos → cria User + redirect para `/accounts/login/` ✓
- [ ] `POST /accounts/register/` dados inválidos → HTTP 200 + erros no form ✓
- [ ] `POST /accounts/login/` credenciais válidas → redirect para `/dashboard/` ✓
- [ ] `POST /accounts/login/` credenciais inválidas → HTTP 200 + erro ✓
- [ ] `POST /accounts/logout/` → redirect para `/` ou `/accounts/login/` ✓

#### Testes E2E Playwright (opcional nesta fase)
- [ ] Ler `.github/skills/playwright-automation/SKILL.md`
- [ ] Fluxo completo: landing → register → login → dashboard

---

### Dependencies
- [ ] Verificar se `accounts` está em `INSTALLED_APPS`
- [ ] Verificar `requirements/requirements.txt` — nenhum pacote novo necessário nesta fase
- [ ] Confirmar Alpine.js CDN no `base.html`

---

### Git
- [ ] Ler `.github/skills/git-workflow/SKILL.md`
- [ ] Stage apenas arquivos relacionados a esta fase
- [ ] Commit Conventional: `feat(core): add LandingPageView`
- [ ] Commit Conventional: `feat(accounts): add authentication (login, register, logout)`
- [ ] Commit Conventional: `feat(frontend): landing page glassmorphism dark design`
- [ ] Push para branch `feat/fase-1-5-landing-autenticacao`

---

## Riscos e Premissas

- **Risco**: Alpine.js e Tailwind CDN podem conflitar com CSP headers — verificar `base.html` existente
- **Risco**: `UserCreationForm` padrão do Django usa campos em inglês — considerar override para PT-BR
- **Premissa**: `fintrack/urls.py` já inclui rota para `dashboard/` (Fase 1 concluída)
- **Premissa**: `base.html` já tem estrutura de blocos (`{% block content %}`)
- **Premissa**: Tailwind CSS já está configurado no projeto (CDN ou build)

---

## Definition of Done (DoD)

- [ ] URL `/` retorna HTTP 200 com template correto
- [ ] URLs `/accounts/login/` e `/accounts/register/` retornam HTTP 200
- [ ] Registro cria usuário no banco e redireciona para login
- [ ] Login com credenciais válidas redireciona para `/dashboard/`
- [ ] Mockup na landing exibe "Entradas" em verde e "Saídas" em vermelho
- [ ] Design responsivo validado nos 3 breakpoints
- [ ] Todos os testes pytest passando (`pytest --tb=short`)
- [ ] Code review concluído (sem violações PEP8/segurança)
- [ ] Commits realizados seguindo git-workflow
- [ ] Sem itens bloqueados

---

## Log de Progresso

- 2026-03-25: Plano criado pelo Planner Checklist. Pronto para início da implementação.
