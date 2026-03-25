# Plano: Fase 1 - Setup, Estrutura Base e Dashboard

**Data:** 2026-03-25
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Configurar o projeto Django `fintrack` com apps `core`, `finances` e `dashboard`, implementar os selectors de dados do dashboard, as CBVs com fragmentos HTMX e o template principal com ApexCharts em modo dark.

---

## Escopo

### Incluido
- Criacao do projeto Django 5.x com apps `core`, `finances`, `dashboard`
- Arquivos `services.py` e `selectors.py` em cada app (Arquitetura Limpa)
- 4 selectors no `dashboard` (evolucao 6 meses, distribuicao saidas, metas mockadas, investimentos mockados)
- 4 CBVs HTMX retornando fragmentos HTML com ApexCharts
- Template principal com lazy loading HTMX
- Cards premium com Tailwind CSS dark mode
- Testes pytest HTTP 200 para todas as rotas HTMX

### Fora de escopo
- Autenticacao/login de usuarios
- CRUD de Entradas e Saidas
- Persistencia real de dados de metas e investimentos
- DRF, Docker, banco de dados em producao
- Deploy

---

## Checklist de Execucao

### Pre-requisitos
- [ ] Ler skill `django-patterns` (`/.github/skills/django-patterns/SKILL.md`)
- [ ] Ler skill `testing-workflow` (`/.github/skills/testing-workflow/SKILL.md`)
- [ ] Ler skill `frontend-finance-design` (`/.github/skills/frontend-finance-design/SKILL.md`)
- [ ] Ler skill `htmx-patterns` (`/.github/skills/htmx-patterns/SKILL.md`)
- [ ] Django 5.x instalado (`pip install django`)
- [ ] pytest-django configurado (`pip install pytest-django pytest`)
- [ ] `pytest.ini` ou `pyproject.toml` com `DJANGO_SETTINGS_MODULE` apontando para `fintrack.settings`

---

### Backend

#### Estrutura do Projeto
- [ ] Criar projeto Django: `django-admin startproject fintrack .`
- [ ] Criar app `core`: `python manage.py startapp core`
- [ ] Criar app `finances`: `python manage.py startapp finances`
- [ ] Criar app `dashboard`: `python manage.py startapp dashboard`
- [ ] Registrar os 3 apps em `INSTALLED_APPS` no `settings.py`
- [ ] Criar `core/services.py` (vazio, placeholder Arquitetura Limpa)
- [ ] Criar `core/selectors.py` (vazio, placeholder Arquitetura Limpa)
- [ ] Criar `finances/services.py` (vazio, placeholder Arquitetura Limpa)
- [ ] Criar `finances/selectors.py` (vazio, placeholder Arquitetura Limpa)
- [ ] Criar `dashboard/services.py` (vazio, placeholder Arquitetura Limpa)
- [ ] Criar `dashboard/selectors.py` com os 4 selectors principais

#### Modelo de Dados (`finances`)
- [ ] **[RED]** Escrever teste: model `Transacao` com campos `tipo` (entrada/saida), `valor`, `categoria`, `data`, `usuario`
- [ ] **[GREEN]** Criar model `Transacao` em `finances/models.py`
- [ ] **[RED]** Escrever teste: model `Categoria` com campo `nome` e FK para usuario
- [ ] **[GREEN]** Criar model `Categoria` em `finances/models.py`
- [ ] Rodar `python manage.py makemigrations finances`
- [ ] Rodar `python manage.py migrate`

#### Selectors (`dashboard/selectors.py`)
- [ ] **[RED]** Escrever teste para `obter_dados_evolucao_6_meses(user)`:
  - Verificar que retorna lista com os ultimos 6 meses
  - Verificar chaves `mes`, `entradas`, `saidas` em cada item
  - Verificar agrupamento correto com `TruncMonth` + `Sum`
- [ ] **[GREEN]** Implementar `obter_dados_evolucao_6_meses(user)` em `dashboard/selectors.py`
- [ ] **[RED]** Escrever teste para `obter_distribuicao_saidas_mes(user)`:
  - Verificar que retorna saidas do mes atual agrupadas por categoria
  - Verificar chaves `categoria`, `total` em cada item
- [ ] **[GREEN]** Implementar `obter_distribuicao_saidas_mes(user)` em `dashboard/selectors.py`
- [ ] **[RED]** Escrever teste para `obter_dados_metas(user)`:
  - Verificar que retorna lista de metas com dados mockados
  - Verificar chaves `nome`, `progresso`, `meta` em cada item
- [ ] **[GREEN]** Implementar `obter_dados_metas(user)` com dados mockados
- [ ] **[RED]** Escrever teste para `obter_dados_investimentos(user)`:
  - Verificar que retorna lista de investimentos com dados mockados
  - Verificar chaves `nome`, `valor`, `percentual` em cada item
- [ ] **[GREEN]** Implementar `obter_dados_investimentos(user)` com dados mockados
- [ ] Refatorar selectors: garantir uso de `select_related`/`prefetch_related` onde aplicavel

#### CBVs HTMX (`dashboard/views.py`)
- [ ] **[RED]** Escrever teste HTTP 200 para `GraficoEvolucaoView` (GET `/dashboard/graficos/evolucao/`)
- [ ] **[GREEN]** Implementar `GraficoEvolucaoView` (TemplateView) chamando `obter_dados_evolucao_6_meses`
- [ ] **[RED]** Escrever teste HTTP 200 para `GraficoSaidasView` (GET `/dashboard/graficos/saidas/`)
- [ ] **[GREEN]** Implementar `GraficoSaidasView` (TemplateView) chamando `obter_distribuicao_saidas_mes`
- [ ] **[RED]** Escrever teste HTTP 200 para `GraficoMetasView` (GET `/dashboard/graficos/metas/`)
- [ ] **[GREEN]** Implementar `GraficoMetasView` (TemplateView) chamando `obter_dados_metas`
- [ ] **[RED]** Escrever teste HTTP 200 para `GraficoInvestimentosView` (GET `/dashboard/graficos/investimentos/`)
- [ ] **[GREEN]** Implementar `GraficoInvestimentosView` (TemplateView) chamando `obter_dados_investimentos`
- [ ] Configurar `dashboard/urls.py` com as 4 rotas HTMX
- [ ] Incluir `dashboard/urls.py` no `fintrack/urls.py`

#### Code Review Backend
- [ ] Ler skill `code-review` (`/.github/skills/code-review/SKILL.md`)
- [ ] Verificar: sem imports nao utilizados em `views.py`, `selectors.py`, `models.py`
- [ ] Verificar: sem logica de negocio nas views (apenas chamada ao selector)
- [ ] Verificar: PEP8 em todos os arquivos `.py` modificados
- [ ] Verificar: terminologia correta — "Entradas" (nunca "receitas"), "Saidas" (nunca "despesas")

---

### Frontend

#### Templates de Fragmentos HTMX
- [ ] Ler skill `frontend-finance-design` e `htmx-patterns`
- [ ] Criar `templates/dashboard/fragmentos/grafico_evolucao.html`:
  - Container com `id` unico para ApexCharts
  - Script inline inicializando grafico de area suave
  - Entradas: `#4ADE80` (verde) com gradiente, Saidas: `#F87171` (vermelho) com gradiente
  - Fundo transparente, tema dark, sem borda
- [ ] Criar `templates/dashboard/fragmentos/grafico_saidas.html`:
  - Donut chart com distribuicao de Saidas por categoria
  - Paleta de cores coesa com o tema dark
- [ ] Criar `templates/dashboard/fragmentos/grafico_metas.html`:
  - Donut chart com progresso das metas
- [ ] Criar `templates/dashboard/fragmentos/grafico_investimentos.html`:
  - Donut chart com distribuicao de investimentos

#### Template Principal do Dashboard
- [ ] Criar `templates/dashboard/index.html` extendendo `base.html`
- [ ] Incluir ApexCharts via CDN: `<script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>`
- [ ] Incluir HTMX via CDN: `<script src="https://unpkg.com/htmx.org@2.x"></script>`
- [ ] Implementar secao de cards de resumo (Entradas e Saidas do mes):
  - `bg-slate-800`, `rounded-2xl`, `border border-slate-700/50`, `shadow-xl`, `p-6`
- [ ] Implementar secao do grafico de evolucao:
  - Container com `hx-get="/dashboard/graficos/evolucao/"` e `hx-trigger="load"`
  - Spinner de loading como placeholder
- [ ] Implementar secao dos 3 donuts lado a lado:
  - Containers com `hx-get` apontando para as 3 rotas de donuts
  - `hx-trigger="load"` em cada um
- [ ] Criar `templates/base.html` com estrutura HTML5, Tailwind CDN, dark mode (`class="dark"`)

#### Responsividade e Acessibilidade
- [ ] Verificar layout em mobile (coluna unica)
- [ ] Verificar layout em desktop (grid multi-coluna)
- [ ] Atributos `aria-label` nos containers dos graficos

---

### Testes

#### Configuracao
- [ ] Criar `pytest.ini` com `DJANGO_SETTINGS_MODULE = fintrack.settings`
- [ ] Criar `conftest.py` com fixture `user` (usuario autenticado para testes)
- [ ] Criar `conftest.py` com fixture `client_logado` (client com login)

#### Testes de Infraestrutura
- [ ] Teste: apps `core`, `finances`, `dashboard` estao em `INSTALLED_APPS`
- [ ] Teste: banco de dados responde (smoke test)

#### Testes de Selectors
- [ ] Teste `obter_dados_evolucao_6_meses`: retorna exatamente 6 itens
- [ ] Teste `obter_dados_evolucao_6_meses`: soma de entradas/saidas por mes correta (com fixtures de Transacao)
- [ ] Teste `obter_distribuicao_saidas_mes`: retorna apenas transacoes do mes atual
- [ ] Teste `obter_distribuicao_saidas_mes`: agrupamento por categoria correto
- [ ] Teste `obter_dados_metas`: retorna lista nao vazia com chaves corretas
- [ ] Teste `obter_dados_investimentos`: retorna lista nao vazia com chaves corretas

#### Testes de Views (HTTP)
- [ ] Ler skill `testing-workflow`
- [ ] Teste HTTP 200: `GET /dashboard/graficos/evolucao/`
- [ ] Teste HTTP 200: `GET /dashboard/graficos/saidas/`
- [ ] Teste HTTP 200: `GET /dashboard/graficos/metas/`
- [ ] Teste HTTP 200: `GET /dashboard/graficos/investimentos/`
- [ ] Teste HTTP 200: `GET /dashboard/` (pagina principal)

#### Testes E2E Playwright (opcional nesta fase)
- [ ] Ler skill `playwright-automation`
- [ ] Smoke test: pagina do dashboard carrega sem erros de console
- [ ] Verificar que os 4 graficos sao renderizados apos HTMX lazy load

---

### Dependencies
- [ ] `requirements/requirements.txt` criado com:
  - `django>=5.0`
  - `pytest-django`
  - `pytest`
  - `whitenoise` (servir staticfiles)
- [ ] `pip install -r requirements/requirements.txt` executado sem erros

---

### Documentacao
- [ ] README Curator invocado (atualizar `README.md` com instrucoes de setup da Fase 1)
- [ ] Secao "Como rodar localmente" com `python manage.py runserver`
- [ ] Secao "Como rodar testes" com `pytest`

---

## Riscos e Premissas
- **Risco**: ApexCharts com HTMX pode exigir re-inicializacao do grafico apos swap — usar evento `htmx:afterSwap` se necessario
- **Risco**: TruncMonth pode variar conforme banco de dados (SQLite em dev vs PostgreSQL em prod)
- **Premissa**: Autenticacao nao e escopo desta fase; views podem usar `LoginRequiredMixin` como placeholder ou ter acesso livre em dev
- **Premissa**: Dados mockados para metas e investimentos sao suficientes para validar o layout visual
- **Premissa**: Tailwind CSS e carregado via CDN (sem build step nesta fase)

---

## Log de Progresso
- 2026-03-25: Plano criado pelo Planner Checklist. Fase 1 iniciada.

---

## Validacao Final
- [ ] Todos os itens do checklist marcados como `[x]`
- [ ] `pytest` rodando sem falhas (`PASSED` em todos os testes)
- [ ] Dashboard abre no browser com os 4 graficos carregados via HTMX
- [ ] Nenhum erro de console JavaScript na pagina do dashboard
- [ ] README atualizado com instrucoes da Fase 1
- [ ] Sem itens bloqueados
