---
name: htmx-patterns
description: HTMX + Django patterns for interactive UX without JavaScript complexity. Avoid JS conflicts using HTMX as single source of interactivity.
instructions: |
  Use this skill when building interactive transaction filters, live search, dynamic forms, or paginated lists.
  Follow HTMX + Django patterns to keep JavaScript minimal and avoid conflicts.
  
  Key principle: **HTMX replaces JS** — use HTMX attributes instead of onclick/onchange handlers.
keywords: [htmx, django, interactive-ui, filters, live-search, pagination, forms]
relatedSkills: [django-patterns, frontend-finance-design]
---

# HTMX + Django Patterns

**Goal:** Interactive transaction UI (filters, search, pagination) using HTMX + Django, avoiding JavaScript complexity and conflicts.

## Quick Start

### 1. Install HTMX

HTML template:
```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>

<!-- HTMX defaults for this project -->
<script>
  htmx.config.defaultIndicatorStyle = "spinner";
  htmx.config.timeout = 5000;
</script>
```

### 2. Core Principle: Replace JS

❌ **Bad**: onclick handlers + JavaScript
```html
<button onclick="filterByCategory(5)">Salário</button>
<script>
  function filterByCategory(id) {
    fetch('/api/transactions/?category=' + id)
      .then(r => r.text())
      .then(html => {
        document.getElementById('list').innerHTML = html;
      });
  }
</script>
```

✅ **Good**: HTMX only
```html
<button hx-get="/transactions/filter/" 
        hx-vals='{"category": 5}'
        hx-target="#transaction-list"
        hx-swap="innerHTML">
  Salário
</button>
```

## HTMX Attributes Cheatsheet

```html
<!-- Loading -->
hx-get="/endpoint/"           <!-- GET request -->
hx-post="/endpoint/"          <!-- POST request -->
hx-put="/endpoint/"           <!-- PUT request -->
hx-delete="/endpoint/"        <!-- DELETE request -->

<!-- Target & Swap -->
hx-target="#id"               <!-- Replace this element -->
hx-target="closest .card"     <!-- Find closest .card and replace -->
hx-swap="innerHTML"           <!-- Replace content (default) -->
hx-swap="outerHTML"           <!-- Replace element itself -->
hx-swap="beforeend"           <!-- Append at end -->
hx-swap="afterbegin"          <!-- Prepend at start -->

<!-- Triggering -->
hx-trigger="click"            <!-- On click (default) -->
hx-trigger="change"           <!-- On change (filters, selects) -->
hx-trigger="submit"           <!-- On form submit -->
hx-trigger="every 2s"         <!-- Polling every 2 seconds -->
hx-trigger="key[Enter]"       <!-- Only on Enter key -->

<!-- Data & Values -->
hx-vals='{"key": "value"}'    <!-- Add custom data -->
hx-include="[name=*]"         <!-- Include form fields -->
hx-confirm="Sure?"            <!-- Show confirmation -->

<!-- Indicators & Feedback -->
hx-indicator="#spinner"       <!-- Show loading spinner -->
hx-disabled-elt="this"        <!-- Disable button during request -->
hx-select="#target"           <!-- Select only part of response -->
```

## View Patterns (Django)

### 1. Filter View (CBV compatible)

```python
# views.py
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render
from .models import Transaction

class TransactionFilterView(View):
    """Handle HTMX filter requests"""
    
    def get(self, request):
        queryset = Transaction.objects.filter(user=request.user)
        
        # Apply filters from query params
        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        tipo = request.GET.get('tipo')
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        start_date = request.GET.get('start_date')
        if start_date:
            queryset = queryset.filter(data__gte=start_date)
        
        # Paginate if needed
        page = request.GET.get('page', 1)
        from django.core.paginator import Paginator
        paginator = Paginator(queryset, 20)
        transactions = paginator.get_page(page)
        
        context = {
            'transactions': transactions,
            'page_obj': transactions,
        }
        return render(request, 'transactions/list-items.html', context)
```

### 2. Live Search View

```python
class TransactionSearchView(View):
    """Live search as user types"""
    
    def get(self, request):
        q = request.GET.get('q', '')
        
        if len(q) < 2:
            return render(request, 'transactions/search-results.html', {
                'transactions': [],
            })
        
        # Search descricao or categoria
        from django.db.models import Q
        queryset = Transaction.objects.filter(
            user=request.user
        ).filter(
            Q(descricao__icontains=q) | 
            Q(categoria__nome__icontains=q)
        )[:10]
        
        context = {'transactions': queryset}
        return render(request, 'transactions/search-results.html', context)
```

### 3. Dynamic Form Selects

```python
class SubcategoryView(View):
    """Update subcategories when category changes"""
    
    def get(self, request):
        category_id = request.GET.get('category_id')
        
        if not category_id:
            subcategories = []
        else:
            from .models import Subcategory
            subcategories = Subcategory.objects.filter(
                category_id=category_id
            )
        
        context = {'subcategories': subcategories}
        return render(request, 'transactions/subcategories-select.html', context)
```

## Template Patterns

### 1. Filter Buttons

```html
{% comment %} transactions/filters.html {% endcomment %}
<div class="filter-buttons">
  <button hx-get="{% url 'transactions:filter' %}" 
          hx-vals='{"categoria": ""}'
          hx-target="#transaction-list"
          class="btn btn-sm">
    Todas
  </button>
  
  {% for category in categories %}
    <button hx-get="{% url 'transactions:filter' %}" 
            hx-vals='{"categoria": {{ category.id }} }'
            hx-target="#transaction-list"
            class="btn btn-sm">
      {{ category.nome }}
    </button>
  {% endfor %}
</div>
```

### 2. Live Search Input

```html
{% comment %} transactions/search.html {% endcomment %}
<input type="text" 
       placeholder="Buscar transações..."
       hx-get="{% url 'transactions:search' %}"
       hx-trigger="keyup changed delay:300ms"
       hx-target="#search-results"
       name="q"
       class="form-input full-width">

<div id="search-results"></div>
{% comment %} Results render here from search-results.html {% endcomment %}
```

### 3. Dynamic Form (Dependent Selects)

```html
{% comment %} transactions/form.html {% endcomment %}
<form hx-post="{% url 'transactions:create' %}"
      hx-target="#form-errors"
      hx-swap="innerHTML">
  {% csrf_token %}
  
  <!-- Category select -->
  <select name="category" 
          hx-get="{% url 'transactions:subcategories' %}"
          hx-target="#subcategory-group"
          hx-trigger="change">
    <option>Selecione...</option>
    {% for cat in categories %}
      <option value="{{ cat.id }}">{{ cat.nome }}</option>
    {% endfor %}
  </select>
  
  <!-- Subcategories (updated by htmx) -->
  <div id="subcategory-group">
    <select name="subcategory">
      <option>Selecione categoria primeiro</option>
    </select>
  </div>
  
  <input type="number" name="valor" step="0.01" required>
  <input type="date" name="data" required>
  
  <button type="submit" hx-disabled-elt="this">
    Criar
  </button>
</form>
```

### 4. Pagination

```html
{% comment %} transactions/pagination.html {% endcomment %}
<div id="transaction-list">
  {% include "transactions/list-items.html" %}
</div>

{% comment %} Pagination links use HTMX {% endcomment %}
<div class="pagination">
  {% if page_obj.has_previous %}
    <a hx-get="{% url 'transactions:filter' %}"
       hx-vals='{"page": {{ page_obj.previous_page_number }} }'
       hx-target="#transaction-list"
       class="btn">
      ← Anterior
    </a>
  {% endif %}
  
  <span>Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span>
  
  {% if page_obj.has_next %}
    <a hx-get="{% url 'transactions:filter' %}"
       hx-vals='{"page": {{ page_obj.next_page_number }} }'
       hx-target="#transaction-list"
       class="btn">
      Próxima →
    </a>
  {% endif %}
</div>
```

## Avoid JavaScript Conflicts

### ✅ Do This

```html
<!-- HTMX triggers interaction -->
<button hx-post="/delete/"
        hx-confirm="Deletar?"
        hx-target="closest tr"
        hx-swap="outerHTML swap:1s">
  Deletar
</button>
```

### ❌ Never Do This

```html
<!-- Don't mix JS + HTMX -->
<button onclick="deleteTransaction(5)"
        hx-post="/delete/">  This conflicts!
  Deletar
</button>

<!-- Don't use jQuery with HTMX -->
<button class="delete-btn">Deletar</button>
<script>
  $('.delete-btn').click(function() { ... }) // Conflict!
</script>
```

### Workaround: If External JS Exists

Use HTMX events to notify external code:

```javascript
// external-listeners.js
document.addEventListener('htmx:afterSwap', function(detail) {
  // React to HTMX swap if you must
  console.log('Content swapped:', detail.detail);
});
```

But **prefer HTMX only** — avoid this complexity.

## Integration with @django-patterns

Combine with CBV mixins:

```python
# views.py using @django-patterns mixins
from django.contrib.auth.mixins import LoginRequiredMixin

class TransactionFilterView(LoginRequiredMixin, View):
    """HTMX filter + auth"""
    
    def get(self, request):
        queryset = Transaction.objects.filter(user=request.user)
        # ... filtering logic ...
        return render(request, 'transactions/list-items.html', context)
```

Use in URLs:

```python
# urls.py
urlpatterns = [
    path('transactions/filter/', TransactionFilterView.as_view(), 
         name='filter'),
    path('transactions/search/', TransactionSearchView.as_view(), 
         name='search'),
]
```

## Styling with @frontend-finance-design

Combine HTMX with Tailwind:

```html
<!-- hx-indicator spinner -->
<div id="spinner" class="htmx-indicator hidden">
  <div class="spinner-border animate-spin inline-block 
              w-4 h-4 border-2 border-blue-500 
              border-t-transparent rounded-full"></div>
</div>

<!-- HTMX request shows spinner -->
<button hx-post="/create/"
        hx-indicator="#spinner"
        class="btn btn-primary">
  Criar
</button>
```

## URLs Configuration

```python
# urls.py - transaction app
from .views import (
    TransactionFilterView,
    TransactionSearchView,
    SubcategoryView,
)

app_name = 'transactions'
urlpatterns = [
    path('filter/', TransactionFilterView.as_view(), name='filter'),
    path('search/', TransactionSearchView.as_view(), name='search'),
    path('subcategories/', SubcategoryView.as_view(), name='subcategories'),
]
```

## Performance Tips

1. **Minimize HTML responses** — return only changed elements
2. **Cache category/subcategory lists** — they don't change often
3. **Limit search results to 10** — use `[:10]` in queries
4. **Debounce search** — `hx-trigger="keyup changed delay:300ms"`
5. **Use pagination** — don't load 1000s of items

## Debugging HTMX

```html
<!-- Enable HTMX debug in console -->
<script>
  htmx.logAll();  // See all HTMX events
</script>

<!-- Or in browser DevTools Console -->
htmx.logAll();
```

Watch requests in **Network tab** → filter by `/filter`, `/search`, etc.

## Checklist

- [ ] HTMX script loaded in base template
- [ ] All interactive buttons use `hx-*` (no onclick)
- [ ] Views return HTML partials (not full pages)
- [ ] Proper `hx-target` for each action
- [ ] Loading indicators with `hx-indicator`
- [ ] No JavaScript event listeners duplicating HTMX
- [ ] Filters tested in `/transactions/filter/`
- [ ] Search tested in `/transactions/search/`
- [ ] Pagination loads next page without full reload

---

**Next Steps:**
- [HTMX + Django Views: Detailed Patterns](assets/django-views-htmx.md)
- [HTMX Attribute Reference](assets/htmx-attributes.md)
- [Component Examples: Filters, Search, Pagination](assets/component-examples.md)
- Use [@django-patterns](link-to-skill:/django-patterns) for CBV structure
- Use [@frontend-finance-design](link-to-skill:/frontend-finance-design) for styling
