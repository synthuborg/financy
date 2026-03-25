# Fase 7 — Módulos de Conta Corrente e Cartão de Crédito

**Data:** 2026-03-25
**Track:** Backend + Frontend + Testes
**Status:** Concluída ✅

---

## Contexto

Fase 7 expande o módulo Account do FinTrack, implementando visualização de saldo por conta
e separando o CRUD de Contas Correntes do CRUD de Cartões de Crédito. Adiciona o seletor
`get_account_balance` para cálculo isolado por conta, e atualiza a navegação lateral.

**Base:** 130 testes passando (zero falhas) pós-Fase 6.

---

## Checklist Backend

- [x] `finances/selectors.py`: criar `get_account_balance(account_id, user)` — retorna Decimal
  - Conta Corrente / Carteira: `sum(entradas) - sum(saídas)`
  - Cartão de Crédito: `sum(saídas)` = fatura atual
- [x] `finances/views.py`: criar `ContaCorrenteListView` — queryset: tipo in ['conta_corrente', 'carteira'], injeta dict saldos no context
- [x] `finances/views.py`: criar `ContaCorrenteCreateView` — força tipo_choices sem cartao_credito
- [x] `finances/views.py`: criar `ContaCorrenteUpdateView` — scoped por usuario + tipos corretos
- [x] `finances/views.py`: criar `ContaCorrenteDeleteView` — scoped por usuario
- [x] `finances/views.py`: criar `CartaoCreditoListView` — queryset: tipo='cartao_credito', injeta faturas no context
- [x] `finances/views.py`: criar `CartaoCreditoCreateView` — força tipo='cartao_credito' no form_valid
- [x] `finances/views.py`: criar `CartaoCreditoUpdateView` — scoped por usuario
- [x] `finances/views.py`: criar `CartaoCreditoDeleteView` — scoped por usuario
- [x] `finances/urls.py`: adicionar rotas para conta-corrente e cartao-credito (8 novas)

---

## Checklist Frontend

- [x] `core/templates/base.html`: substituir link "Contas" por "Contas Correntes" + "Cartões" no menu
- [x] `finances/templates/finances/conta_corrente_list.html`: criar template com saldo (text-green-400 positivo, text-red-400 negativo)
- [x] `finances/templates/finances/cartao_credito_list.html`: criar template com fatura (text-red-400)
- [x] `finances/templates/finances/account_form.html`: verificar que funciona para os novos create/update views
- [x] `finances/templates/finances/account_confirm_delete.html`: verificar que funciona para os novos delete views

---

## Checklist Testes

- [x] `finances/tests.py`: `TestGetAccountBalance` — testes para get_account_balance
  - saldo de conta corrente com entradas/saídas
  - fatura de cartão de crédito (apenas saídas)
  - conta sem transações retorna Decimal('0')
  - não vaza dados entre usuários (outro usuário recebe 404)
- [x] `finances/tests.py`: `TestContaCorrenteViews` — HTTP tests para as novas views
  - list retorna 200 para usuário autenticado
  - list requer login
  - create GET/POST
- [x] `finances/tests.py`: `TestCartaoCreditoViews` — HTTP tests
  - list retorna 200 para usuário autenticado
  - create GET/POST

---

## Checklist README

- [x] Atualizar count de testes (151 testes passando)
- [x] Adicionar seção "Fase 7 — Status" ao README
- [x] Badge de fase 7 concluída adicionado
- [x] Badge de testes atualizado de 130 → 151

---

## Riscos

- **Risco:** Saldo calculado em Python via `get_account_balance()` — OK para volume atual (MVP)
- **Risco:** Formulário compartilhado `account_form.html` deve funcionar para ambos os tipos
- **Risco:** URLs antigas para `finances:account_list` ainda funcionam (não quebrar links)
- **Risco:** Vazamento entre usuários — `filter(usuario=request.user)` obrigatório em todos os querysets

---

## Log de Progresso

- 2026-03-25: Plano criado. Escopo definido para seletor de saldo, CBVs separadas por tipo, nav atualizada.
- 2026-03-25: Implementação concluída. 21 novos testes adicionados. 151 testes passando.

---

## Validação Final

- [x] Todos os itens do checklist marcados `[x]`
- [x] Suite de testes passando (151 testes, zero falhas)
- [x] Navegação: links "Contas Correntes" e "Cartões" visíveis no menu lateral
- [x] Saldo exibido em cada conta na listagem (verde para positivo, vermelho para negativo/fatura)
- [x] Sem vazamento de dados entre usuários (escopo garantido)
- [x] Terminologia Entradas/Saídas intacta em todos os templates
- [x] Sem `print()`, `TODO` críticos ou código morto no diff
