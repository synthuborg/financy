---
name: code-review
description: Code review checklist for hackaton_app_financas. Identify and fix: duplicate code, dead code, unnecessary comments, unused imports, complexity, PEP08 violations, and security issues.
instructions: |
  When reviewing code, run through each checklist section in order.
  For each issue found: show the problem, explain why it's an issue, and provide the refactored version.
  Focus on Python/Django, HTML templates, HTMX, and Tailwind CSS.
keywords: [code-review, dry, refactoring, dead-code, pep08, security, clean-code]
---

# Code Review — hackaton_app_financas

Checklist completo para revisar código do projeto. Analisa problemas e entrega código refatorado.

## Como Usar

```
Revise este código:
[colar código aqui]
```

O review retorna:
1. **Problemas encontrados** (com severidade)
2. **Análise de cada item**
3. **Código refatorado** pronto para substituir

---

## Checklist de Revisão

### 🔴 Crítico (corrigir antes de commit)

#### 1. Segurança
- [ ] Hardcoded credentials (`SECRET_KEY`, passwords, tokens em código)
- [ ] SQL injection (query com `%s % valor` em vez de parâmetros)
- [ ] XSS em templates (usar `{{ var }}` com autoescaping, evitar `| safe` sem validação)
- [ ] Dados do usuário sem verificação de ownership

```python
# ❌ SQL injection
cursor.execute(f"SELECT * FROM transactions WHERE id = {user_input}")

# ✅ Parametrizado
cursor.execute("SELECT * FROM transactions WHERE id = %s", [user_input])

# ❌ Hardcoded secret
SECRET_KEY = "minha-chave-secreta"

# ✅ Via environment
SECRET_KEY = os.environ.get('SECRET_KEY')

# ❌ Sem ownership check
transaction = Transaction.objects.get(pk=pk)

# ✅ Com ownership
transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
```

---

### 🟠 Alto (corrigir em PR)

#### 2. Código Duplicado (DRY)

Detectar blocos repetidos de 3+ linhas.

```python
# ❌ Código duplicado
class EntradaListView(LoginRequiredMixin, View):
    def get(self, request):
        queryset = Transaction.objects.filter(user=request.user, tipo='entrada')
        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        return render(request, 'list.html', {'transactions': queryset})

class SaidaListView(LoginRequiredMixin, View):
    def get(self, request):
        queryset = Transaction.objects.filter(user=request.user, tipo='saida')
        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        return render(request, 'list.html', {'transactions': queryset})

# ✅ Extraído em mixin/base
class BaseTransactionListView(LoginRequiredMixin, View):
    tipo = None  # Override in subclass

    def get_queryset(self, request):
        queryset = Transaction.objects.filter(user=request.user)
        if self.tipo:
            queryset = queryset.filter(tipo=self.tipo)
        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset

    def get(self, request):
        return render(request, 'list.html', {
            'transactions': self.get_queryset(request),
        })

class EntradaListView(BaseTransactionListView):
    tipo = 'entrada'

class SaidaListView(BaseTransactionListView):
    tipo = 'saida'
```

#### 3. Imports Não Utilizados

```python
# ❌ Imports desnecessários
from django.shortcuts import render, get_object_or_404, redirect  # redirect não usado
from django.contrib.auth.models import User  # não usado
import json  # não usado
from .models import Transaction, Category  # Category não usada

# ✅ Apenas o necessário
from django.shortcuts import render, get_object_or_404
from .models import Transaction
```

#### 4. Complexidade Excessiva (>20 linhas numa função)

```python
# ❌ Função muito longa (40+ linhas, múltiplas responsabilidades)
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    
    transactions = Transaction.objects.filter(user=request.user)
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    category = request.GET.get('category')
    
    if start:
        transactions = transactions.filter(data__gte=start)
    if end:
        transactions = transactions.filter(data__lte=end)
    if category:
        transactions = transactions.filter(category_id=category)
    
    total_entrada = sum(t.valor for t in transactions if t.tipo == 'entrada')
    total_saida = sum(t.valor for t in transactions if t.tipo == 'saida')
    saldo = total_entrada - total_saida
    
    page = request.GET.get('page', 1)
    paginator = Paginator(transactions, 20)
    page_obj = paginator.get_page(page)
    
    categories = Category.objects.filter(user=request.user)
    
    return render(request, 'dashboard.html', {
        'transactions': page_obj,
        'saldo': saldo,
        'total_entrada': total_entrada,
        'total_saida': total_saida,
        'categories': categories,
    })

# ✅ Responsabilidades separadas
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        queryset = self._filter_transactions(request)
        page_obj = self._paginate(queryset)
        summary = self._calculate_summary(queryset)

        return render(request, 'dashboard.html', {
            'transactions': page_obj,
            **summary,
            'categories': Category.objects.filter(user=request.user),
        })

    def _filter_transactions(self, request):
        qs = Transaction.objects.filter(user=request.user)
        filters = {
            'data__gte': request.GET.get('start_date'),
            'data__lte': request.GET.get('end_date'),
            'category_id': request.GET.get('category'),
        }
        return qs.filter(**{k: v for k, v in filters.items() if v})

    def _paginate(self, queryset, per_page=20):
        paginator = Paginator(queryset, per_page)
        return paginator.get_page(self.request.GET.get('page', 1))

    def _calculate_summary(self, queryset):
        from django.db.models import Sum
        totals = queryset.aggregate(
            total_entrada=Sum('valor', filter=Q(tipo='entrada')),
            total_saida=Sum('valor', filter=Q(tipo='saida')),
        )
        totals['saldo'] = (totals['total_entrada'] or 0) - (totals['total_saida'] or 0)
        return totals
```

---

### 🟡 Médio (corrigir se der tempo)

#### 5. Código Morto

```python
# ❌ Função não chamada em nenhum lugar
def old_export_function():
    pass  # esquecida

# ❌ Variáveis nunca usadas
def my_view(request):
    user = request.user  # usado
    old_data = None      # nunca referenciado depois
    result = do_something()

# ✅ Remover código morto
def my_view(request):
    result = do_something()
```

#### 6. Comentários Desnecessários

```python
# ❌ Comentários óbvios / commented-out code
def create_transaction(data):
    # Create a transaction
    transaction = Transaction(**data)
    # transaction.save()  # removido para testar
    # old_create_method(transaction)
    transaction.save()
    # Return transaction
    return transaction

# ✅ Sem ruído, código fala por si
def create_transaction(data):
    transaction = Transaction(**data)
    transaction.save()
    return transaction
```

Exceções: comentários para lógica **não óbvia**:
```python
# Agrupa por mês usando truncate (evita loops em Python)
transactions.annotate(mes=TruncMonth('data')).values('mes').annotate(...)
```

#### 7. Violações PEP08 (Python)

```python
# ❌ PEP08 violations
def processarTransacao(valor,descricao,tipo):  # camelCase, sem espaços
    if(valor>0):   # sem espaços ao redor de operadores
        t=Transaction(valor=valor,descricao=descricao,tipo=tipo)  # linha > 79 chars, sem espaços
        t.save()
        return t
    else:
        return None

# ✅ PEP08 compliant
def processar_transacao(valor, descricao, tipo):
    """Cria e salva uma transação."""
    if valor > 0:
        transacao = Transaction(
            valor=valor,
            descricao=descricao,
            tipo=tipo,
        )
        transacao.save()
        return transacao
    return None
```

Checklist PEP08:
- [ ] `snake_case` para funções e variáveis
- [ ] `PascalCase` para classes
- [ ] `UPPER_SNAKE_CASE` para constantes
- [ ] Linhas ≤ 79 chars
- [ ] 2 linhas em branco entre funções no nível do módulo
- [ ] 1 linha em branco entre métodos em classe
- [ ] Espaços ao redor de operadores (`x = y + 1`)
- [ ] Sem espaços em chamadas de função (`func(x, y)`)

#### 8. Lógica Confusa

```python
# ❌ Condicional confusa
def get_status(t):
    return 'positivo' if not (t.valor < 0 or t.tipo != 'entrada') else 'negativo'

# ✅ Clara e legível
def get_status(t):
    if t.tipo == 'entrada' and t.valor > 0:
        return 'positivo'
    return 'negativo'

# ❌ List comprehension ilegível
result = [t.valor for t in Transaction.objects.filter(user=request.user) if t.tipo == 'entrada' and t.data.year == 2024]

# ✅ Quebra em múltiplas linhas
result = [
    t.valor
    for t in Transaction.objects.filter(user=request.user)
    if t.tipo == 'entrada' and t.data.year == 2024
]
```

---

## Revisão por Linguagem

### Python / Django

```
CHECKLIST:
[ ] Imports organizados (stdlib → third-party → local)
[ ] Sem imports não usados
[ ] Funções < 20 linhas (split se maior)
[ ] Classes CBV seguem @django-patterns
[ ] Sem código commented-out
[ ] Nomes descritivos (sem x, y, tmp, data como nomes genéricos)
[ ] Sem hardcoded credentials
[ ] Ownership check em todas as queries de usuário
[ ] Queries eficientes (select_related, prefetch_related)
[ ] PEP08 compliant
```

### HTML / Templates Django

```
CHECKLIST:
[ ] Sem lógica complexa no template (extrair para view/tag)
[ ] Sem classes Tailwind duplicadas (extrair componente)
[ ] Sem IDs duplicados na página
[ ] hx-* HTMX ao invés de onclick
[ ] Campos de form com label e name corretos
[ ] Imagens sem alt="" vazio
[ ] Sem HTML commented-out
[ ] Sem inline styles (usar Tailwind)
```

```html
<!-- ❌ Lógica no template -->
{% if transaction.valor > 0 and transaction.tipo == 'entrada' and not transaction.deleted %}

<!-- ✅ Propriedade no model -->
{% if transaction.is_positive %}
```

```python
# model.py
@property
def is_positive(self):
    return self.tipo == 'entrada' and self.valor > 0 and not self.deleted
```

### JavaScript / HTMX

```
CHECKLIST:
[ ] Sem onclick/onchange - usar hx-trigger
[ ] Sem jQuery misturado com HTMX
[ ] Sem event listeners duplicados
[ ] Sem console.log esquecidos
[ ] Sem scripts inline (exceto configuração inicial)
[ ] Funções JS só se HTMX não resolve
```

```html
<!-- ❌ JS + HTMX conflito -->
<button onclick="submitForm()" hx-post="/create/">Submit</button>
<script>function submitForm() { ... }</script>

<!-- ✅ Só HTMX -->
<button hx-post="/create/" hx-target="#result">Submit</button>
```

### CSS / Tailwind

```
CHECKLIST:
[ ] Sem CSS inline (style="...")
[ ] Sem classes hardcoded de cor (usar variáveis Tailwind)
[ ] Componentes repetidos extraídos ({% include %})
[ ] Responsivo: mobile-first (sem md: sem base)
[ ] Sem classes conflitantes no mesmo elemento
```

```html
<!-- ❌ Classes duplicadas em 5+ lugares -->
<div class="bg-white rounded-lg shadow-md border p-4 hover:shadow-lg">Card 1</div>
<div class="bg-white rounded-lg shadow-md border p-4 hover:shadow-lg">Card 2</div>

<!-- ✅ Extraído em componente -->
{% include "components/card.html" with title="Card 1" %}
{% include "components/card.html" with title="Card 2" %}
```

---

## Severidade e Prioridade

```
🔴 CRÍTICO   → Bloqueia merge. Corrigir agora.
🟠 ALTO      → Deve ser corrigido em PR atual.
🟡 MÉDIO     → Corrigir na próxima sprint se der.
🔵 BAIXO     → Nitpick / style preference.
```

---

## Template de Resposta

Ao revisar código, estruture assim:

```
## Code Review

### Problemas Encontrados

| # | Severidade | Tipo | Linha | Descrição |
|---|-----------|------|-------|-----------|
| 1 | 🔴 Crítico | Segurança | 12 | Ownership não verificado |
| 2 | 🟠 Alto | DRY | 25-40 | Lógica duplicada em 2 views |
| 3 | 🟡 Médio | PEP08 | 8 | Import não usado: `json` |

### Análise e Refatoração

**#1 — Ownership não verificado**
→ [análise] → [código refatorado]

**#2 — DRY: lógica duplicada**
→ [análise] → [código refatorado]

**#3 — Import não usado**
→ [análise] → [código refatorado]

### Código Refatorado Completo
[arquivo completo com todas as correções aplicadas]

### Resumo
- X problemas críticos corrigidos
- Y duplicações removidas
- Linhas de código: antes/depois
```

---

## Integração com Skills

- **@django-patterns** — Use para padrões CBV corretos após review
- **@htmx-patterns** — Use para reescrever JS/onclick com HTMX
- **@frontend-finance-design** — Use para Tailwind consistency
- **@testing-workflow** — Rodar testes após refatoração

---

## Exemplo de Uso

```
Revise este arquivo views.py:

[código]
```

Ou revisar template:

```
Revise este HTML, foco em: classes duplicadas e lógica no template
```

Ou foco específico:

```
Revise este código buscando só DRY violations e imports não usados
```
