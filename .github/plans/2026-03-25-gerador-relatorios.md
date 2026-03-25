# Plano: Gerador de Relatórios Financeiros

**Data:** 2026-03-25
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Criar um gerador de relatórios financeiros humanizados (PDF e Excel) com filtro por período, resumos analíticos, distribuição por categoria e insights — exportáveis via `reportlab` (PDF) e `openpyxl` (Excel).

---

## Escopo

### Incluído
- Nova rota `financas/relatorios/` com formulário de filtro (data_inicio, data_fim, formato)
- Geração de PDF humanizado (cabeçalho FinTrack, resumo financeiro, distribuição por categoria, transações agrupadas, rodapé)
- Geração de Excel com abas "Resumo", "Transações" e "Por Categoria"
- Selector `get_report_data(user, data_inicio, data_fim)` para agregar dados
- Services `generate_pdf_report(user, data_inicio, data_fim)` e `generate_excel_report(user, data_inicio, data_fim)`
- Template com formulário de filtro (date pickers + radio PDF/Excel + botão gerar)
- Item "Relatórios" no sidebar do `base.html`
- Dependências `reportlab` e `openpyxl` no `requirements/requirements.txt`

### Fora de escopo
- Gráficos dentro do PDF
- Envio por email
- Agendamento automático
- Relatório de metas/investimentos

---

## Contexto Técnico Mapeado

| Artefato | Localização | Relevância |
|----------|-------------|------------|
| Models (Transaction, Category, Account) | `finances/models.py` | Fonte de dados — campos: valor, data, tipo, descricao, categoria (FK), conta (FK), usuario (FK) |
| `get_all_transactions(user)` | `finances/selectors.py` | Referência de query com `select_related` |
| `calculate_balance(user)` | `finances/services.py` | Padrão de agregação existente |
| `obter_distribuicao_saidas_mes(user)` | `dashboard/selectors.py` | Referência para distribuição por categoria |
| `obter_resumo_mes_atual(user)` | `dashboard/selectors.py` | Referência para KPIs |
| Sidebar com seções | `core/templates/base.html` | Onde adicionar link "Relatórios" |
| Fixtures `usuario`, `client_autenticado` | `conftest.py` | Fixtures para testes |
| CSS classes (`INPUT_CSS`, `SELECT_CSS`) | `finances/forms.py` | Padrão de estilo para formulários |
| URL namespace `finances` | `finances/urls.py` | Namespace para nova rota |

---

## Checklist de Execução

### 1. Dependências
- [ ] Adicionar `reportlab` e `openpyxl` ao `requirements/requirements.txt`
- [ ] Instalar dependências (`pip install -r requirements/requirements.txt`)

### 2. Backend — Selector (TDD)

**Arquivo:** `finances/selectors.py`
**Função:** `get_report_data(user, data_inicio, data_fim) -> dict`

Retorna:
```python
{
    "periodo": {"inicio": date, "fim": date},
    "total_entradas": Decimal,
    "total_saidas": Decimal,
    "saldo_liquido": Decimal,
    "num_transacoes": int,
    "maior_entrada": Decimal | None,
    "maior_saida": Decimal | None,
    "distribuicao_categorias": [{"categoria": str, "total": Decimal, "percentual": float}, ...],
    "transacoes_por_categoria": {str: [Transaction, ...]},
    "transacoes": QuerySet,
}
```

- [ ] Ler skill `django-patterns`
- [ ] **RED** — Escrever testes em `finances/tests.py`:
  - `test_get_report_data_periodo_vazio` — retorna zeros quando não há transações
  - `test_get_report_data_totais_corretos` — soma entradas e saídas no período
  - `test_get_report_data_filtra_por_periodo` — ignora transações fora do range
  - `test_get_report_data_filtra_por_usuario` — não retorna dados de outro usuário
  - `test_get_report_data_distribuicao_categorias` — calcula percentuais de saída
  - `test_get_report_data_transacoes_agrupadas` — agrupa por categoria
  - `test_get_report_data_maior_entrada_saida` — identifica maiores transações
- [ ] **GREEN** — Implementar `get_report_data` em `finances/selectors.py`
- [ ] Rodar testes e confirmar que todos passam
- [ ] Refatorar se necessário

### 3. Backend — Service PDF (TDD)

**Arquivo:** `finances/services.py`
**Função:** `generate_pdf_report(user, data_inicio, data_fim) -> BytesIO`

Estrutura do PDF:
1. Cabeçalho: "FinTrack — Relatório Financeiro", período, data de geração
2. Resumo: total entradas, total saídas, saldo líquido (caixa destacada)
3. Distribuição por categoria: top categorias de saída com percentual
4. Transações agrupadas por categoria com subtotal
5. Rodapé: "Relatório gerado por FinTrack"

- [ ] **RED** — Escrever testes em `finances/tests.py`:
  - `test_generate_pdf_report_returns_bytes` — retorna BytesIO com conteúdo
  - `test_generate_pdf_report_is_valid_pdf` — começa com `%PDF`
  - `test_generate_pdf_report_empty_period` — gera PDF mesmo sem transações
  - `test_generate_pdf_report_ownership` — não inclui dados de outro usuário
- [ ] **GREEN** — Implementar `generate_pdf_report` em `finances/services.py` usando `reportlab`
- [ ] Confirmar formato monetário brasileiro (`R$ 1.234,56`)
- [ ] Textos do relatório em português
- [ ] Rodar testes e confirmar que todos passam

### 4. Backend — Service Excel (TDD)

**Arquivo:** `finances/services.py`
**Função:** `generate_excel_report(user, data_inicio, data_fim) -> BytesIO`

Estrutura do Excel:
- Aba "Resumo": KPIs (total entradas, saídas, saldo, nº transações, maior entrada, maior saída)
- Aba "Transações": colunas (Data, Tipo, Descrição, Categoria, Conta, Valor)
- Aba "Por Categoria": resumo de gastos por categoria com percentual

- [ ] **RED** — Escrever testes em `finances/tests.py`:
  - `test_generate_excel_report_returns_bytes` — retorna BytesIO com conteúdo
  - `test_generate_excel_report_has_three_sheets` — contém 3 abas
  - `test_generate_excel_report_resumo_sheet` — aba Resumo tem KPIs corretos
  - `test_generate_excel_report_transacoes_sheet` — aba Transações lista dados
  - `test_generate_excel_report_categorias_sheet` — aba Por Categoria tem distribuição
  - `test_generate_excel_report_empty_period` — gera Excel mesmo sem transações
  - `test_generate_excel_report_ownership` — não inclui dados de outro usuário
- [ ] **GREEN** — Implementar `generate_excel_report` em `finances/services.py` usando `openpyxl`
- [ ] Confirmar formato monetário brasileiro
- [ ] Rodar testes e confirmar que todos passam

### 5. Backend — Form

**Arquivo:** `finances/forms.py`
**Classe:** `ReportFilterForm`

Campos:
- `data_inicio` (DateField, widget DateInput type=date)
- `data_fim` (DateField, widget DateInput type=date)
- `formato` (ChoiceField: 'pdf' | 'excel', widget RadioSelect)

Validações:
- `data_inicio` <= `data_fim`
- Período máximo de 1 ano (opcional, mas razoável)

- [ ] **RED** — Escrever testes:
  - `test_report_form_valid` — form válido com dados corretos
  - `test_report_form_invalid_dates` — data_inicio > data_fim é inválido
  - `test_report_form_missing_fields` — campos obrigatórios
- [ ] **GREEN** — Implementar `ReportFilterForm` em `finances/forms.py`
- [ ] Aplicar CSS classes (`INPUT_CSS`, `SELECT_CSS`) conforme padrão do projeto

### 6. Backend — View (TDD)

**Arquivo:** `finances/views.py`
**Classe:** `ReportView(LoginRequiredMixin, View)`

Comportamento:
- `GET`: renderiza template com formulário de filtro
- `POST`: valida formulário, gera relatório (PDF ou Excel), retorna como download (`Content-Disposition: attachment`)

- [ ] **RED** — Escrever testes:
  - `test_report_view_get_authenticated` — retorna 200 com formulário
  - `test_report_view_get_unauthenticated` — redireciona para login
  - `test_report_view_post_pdf` — retorna arquivo PDF com content-type correto
  - `test_report_view_post_excel` — retorna arquivo Excel com content-type correto
  - `test_report_view_post_invalid_form` — re-renderiza com erros
- [ ] **GREEN** — Implementar `ReportView` em `finances/views.py`
- [ ] Registrar rota em `finances/urls.py`: `path('relatorios/', ReportView.as_view(), name='report')`
- [ ] Rodar testes e confirmar que todos passam

### 7. Frontend — Template

**Arquivo:** `finances/templates/finances/report_form.html`

- [ ] Ler skills `frontend-finance-design` e `htmx-patterns`
- [ ] Criar template com:
  - Extends `base.html`
  - Título "Relatórios Financeiros"
  - Formulário com date pickers estilizados (dark mode, Tailwind)
  - Radio buttons PDF/Excel com ícones
  - Botão "Gerar Relatório" com estilo primário
  - Feedback visual (loading state com HTMX indicator, se aplicável)
- [ ] Validar responsividade (mobile-first)
- [ ] Validar acessibilidade (labels, focus states, aria)

### 8. Frontend — Sidebar

**Arquivo:** `core/templates/base.html`

- [ ] Adicionar item "Relatórios" no sidebar (entre Metas e seção de Contas)
- [ ] Usar ícone SVG de documento/relatório
- [ ] Aplicar padrão de active state (`request.resolver_match.url_name == 'report'`)
- [ ] Validar que não quebra layout existente

### 9. Testes de Integração

- [ ] Ler skill `testing-workflow`
- [ ] Testar fluxo completo: login → navegar para relatórios → preencher formulário → baixar PDF
- [ ] Testar fluxo completo: login → navegar para relatórios → preencher formulário → baixar Excel
- [ ] Verificar ownership check end-to-end

### 10. Code Review & Refactor

- [ ] Ler skill `code-review`
- [ ] Revisar: código duplicado, imports não usados, complexidade, PEP08
- [ ] Verificar segurança: ownership check, LoginRequiredMixin, sem exposição de dados
- [ ] Verificar performance: `select_related` nas queries
- [ ] Executar code-review checklist completo

### 11. Git & Documentação

- [ ] Ler skill `git-workflow`
- [ ] Commit com Conventional Commits: `feat(finances): add financial report generator (PDF/Excel)`
- [ ] README Curator invocado (se aplicável)

---

## Arquivos a Criar/Modificar

| Ação | Arquivo |
|------|---------|
| Modificar | `requirements/requirements.txt` — adicionar `reportlab`, `openpyxl` |
| Modificar | `finances/selectors.py` — adicionar `get_report_data()` |
| Modificar | `finances/services.py` — adicionar `generate_pdf_report()`, `generate_excel_report()` |
| Modificar | `finances/forms.py` — adicionar `ReportFilterForm` |
| Modificar | `finances/views.py` — adicionar `ReportView` |
| Modificar | `finances/urls.py` — adicionar rota `relatorios/` |
| Criar | `finances/templates/finances/report_form.html` — template do formulário |
| Modificar | `core/templates/base.html` — adicionar item sidebar |
| Modificar | `finances/tests.py` — adicionar todos os testes |

---

## Riscos e Premissas

- **Risco:** `reportlab` pode ter limitações para layout complexo — mitigar com design simples e funcional
- **Risco:** Performance em períodos longos com muitas transações — mitigar com `select_related` e queries otimizadas
- **Premissa:** SQLite suporta o volume de dados esperado para geração de relatórios
- **Premissa:** Não há necessidade de celery/async — geração é síncrona e rápida para volume esperado
- **Premissa:** Models existentes (Transaction, Category, Account) não precisam de alteração

---

## Ordem de Implementação Recomendada

```
1. Dependências (requirements.txt)
2. Selector (get_report_data) — TDD
3. Service PDF (generate_pdf_report) — TDD
4. Service Excel (generate_excel_report) — TDD
5. Form (ReportFilterForm) — TDD
6. View (ReportView) — TDD
7. Template (report_form.html)
8. Sidebar (base.html)
9. Testes de integração
10. Code review & refactor
11. Git commit
```

---

## Log de Progresso
- 2026-03-25: Plano criado com checklist completo. Contexto técnico mapeado (models, selectors, services, templates, fixtures).

---

## Validação Final
- [ ] Todos os itens do checklist marcados
- [ ] Testes passando (`pytest`)
- [ ] README atualizado
- [ ] Sem itens bloqueados
- [ ] Sidebar funcional com link para relatórios
- [ ] PDF gerado com formato correto e texto em português
- [ ] Excel gerado com 3 abas e dados corretos
- [ ] Formato monetário brasileiro (R$ 1.234,56)
- [ ] Ownership check em todas as queries
- [ ] LoginRequiredMixin na view
