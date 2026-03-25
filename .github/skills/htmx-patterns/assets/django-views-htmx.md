# HTMX + Django Views - Padrões Detalhados

Implementações completas de views para HTMX no hackaton_app_financas.

## 1. Filter View (Múltiplos Filtros)

```python
# transactions/views.py
from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Transaction, Category

class TransactionFilterView(View):
    paginate_by = 20
    template_name = 'transactions/list-items.html'
    
    def get(self, request):
        # Start with user's transactions
        queryset = Transaction.objects.filter(user=request.user).select_related('category')
        
        # Filter 1: Category
        category_id = request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter 2: Type (entrada/saída)
        tipo = request.GET.get('tipo')
        if tipo in ['entrada', 'saida']:
            queryset = queryset.filter(tipo=tipo)
        
        # Filter 3: Date Range
        start_date = request.GET.get('start_date')
        if start_date:
            queryset = queryset.filter(data__gte=start_date)
        
        end_date = request.GET.get('end_date')
        if end_date:
            queryset = queryset.filter(data__lte=end_date)
        
        # Sort
        sort_by = request.GET.get('sort_by', '-data')  # Default newest first
        queryset = queryset.order_by(sort_by)
        
        # Pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, self.paginate_by)
        page_obj = paginator.get_page(page)
        
        context = {
            'transactions': page_obj,
            'page_obj': page_obj,
            'categories': Category.objects.filter(user=request.user),
        }
        
        # Return only list items (partial HTML)
        return render(request, self.template_name, context)
```

**HTML Template** (`transactions/list-items.html`):

```html
{% comment %} Retorna apenas os items da lista {% endcomment %}
{% for t in transactions %}
  <div class="transaction-item border-b py-3 hover:bg-gray-50">
    <div class="flex justify-between items-start">
      <div class="flex-1">
        <p class="font-semibold text-gray-900">{{ t.descricao }}</p>
        <p class="text-sm text-gray-500">{{ t.categoria.nome }}</p>
      </div>
      <div class="text-right">
        <p class="font-bold {% if t.tipo == 'entrada' %}text-green-600{% else %}text-red-600{% endif %}">
          {% if t.tipo == 'entrada' %}+{% else %}-{% endif %}{{ t.valor }}
        </p>
        <p class="text-xs text-gray-400">{{ t.data|date:"d/m/Y" }}</p>
      </div>
    </div>
  </div>
{% empty %}
  <div class="text-center py-8 text-gray-500">
    Nenhuma transação encontrada.
  </div>
{% endfor %}

{% comment %} Pagination links {% endcomment %}
{% if page_obj.has_other_pages %}
  <div class="flex justify-between items-center mt-4 py-4 border-t">
    {% if page_obj.has_previous %}
      <a hx-get="{% url 'transactions:filter' %}"
         hx-vals='{"page": {{ page_obj.previous_page_number }} }'
         hx-target="#transaction-list"
         hx-swap="innerHTML"
         class="btn btn-sm">
        ← Anterior
      </a>
    {% else %}
      <span class="text-gray-400">← Anterior</span>
    {% endif %}
    
    <span class="text-sm text-gray-600">
      Pág {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}
    </span>
    
    {% if page_obj.has_next %}
      <a hx-get="{% url 'transactions:filter' %}"
         hx-vals='{"page": {{ page_obj.next_page_number }} }'
         hx-target="#transaction-list"
         hx-swap="innerHTML"
         class="btn btn-sm">
        Próxima →
      </a>
    {% else %}
      <span class="text-gray-400">Próxima →</span>
    {% endif %}
  </div>
{% endif %}
```

## 2. Live Search View

```python
class TransactionSearchView(View):
    """Live search com debounce"""
    template_name = 'transactions/search-results.html'
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        results = []
        
        # Se query muito curta, retornar vazio
        if len(query) < 2:
            return render(request, self.template_name, {
                'results': results,
                'query': query,
            })
        
        # Buscar em descrição e categoria
        results = Transaction.objects.filter(
            user=request.user
        ).filter(
            Q(descricao__icontains=query) | 
            Q(categoria__nome__icontains=query)
        ).select_related('category')[:10]
        
        context = {
            'results': results,
            'query': query,
        }
        
        return render(request, self.template_name, context)
```

**HTML Template** (`transactions/search-results.html`):

```html
{% if results %}
  <ul class="border rounded-lg shadow-md absolute top-full w-full bg-white z-10">
    {% for result in results %}
      <li class="border-b last:border-b-0 hover:bg-blue-50 cursor-pointer"
          hx-on::click="htmx.ajax('GET', '{% url 'transactions:detail' result.id %}', {target: '#main'})">
        <a class="block px-4 py-2">
          <span class="font-semibold">{{ result.descricao }}</span>
          <span class="text-gray-500 text-sm ml-2">{{ result.categoria.nome }}</span>
          <span class="float-right font-bold {% if result.tipo == 'entrada' %}text-green-600{% else %}text-red-600{% endif %}">
            {{ result.valor }}
          </span>
        </a>
      </li>
    {% endfor %}
  </ul>
{% elif query %}
  <div class="text-center text-gray-500 text-sm py-4">
    Nenhum resultado para "{{ query }}"
  </div>
{% endif %}
```

## 3. Dynamic Form (Dependent Selects)

```python
class SubcategoryView(View):
    """Retorna subcategorias para categoria selecionada"""
    template_name = 'transactions/form-subcategory.html'
    
    def get(self, request):
        category_id = request.GET.get('category_id')
        
        if not category_id:
            subcategories = []
        else:
            from .models import Subcategory
            try:
                subcategories = Subcategory.objects.filter(
                    category_id=int(category_id)
                )
            except (ValueError, TypeError):
                subcategories = []
        
        context = {'subcategories': subcategories}
        return render(request, self.template_name, context)
```

**HTML Template** (`transactions/form-subcategory.html`):

```html
<select name="subcategory" 
        id="subcategory-select"
        class="form-input">
  <option value="">Selecione...</option>
  {% for sub in subcategories %}
    <option value="{{ sub.id }}">{{ sub.nome }}</option>
  {% endfor %}
</select>
```

**Form Template** (`transactions/form.html`):

```html
<form hx-post="{% url 'transactions:create' %}"
      class="space-y-4">
  {% csrf_token %}
  
  <!-- Category (triggers subcategory update) -->
  <div>
    <label class="block text-sm font-medium mb-1">Categoria</label>
    <select name="category_id" 
            id="category-select"
            hx-get="{% url 'transactions:subcategories' %}"
            hx-trigger="change"
            hx-target="#subcategory-group"
            hx-swap="innerHTML"
            class="form-input full-width">
      <option value="">Selecione...</option>
      {% for cat in categories %}
        <option value="{{ cat.id }}">{{ cat.nome }}</option>
      {% endfor %}
    </select>
  </div>
  
  <!-- Subcategory (updated by HTMX) -->
  <div id="subcategory-group">
    <label class="block text-sm font-medium mb-1">Subcategoria</label>
    <select name="subcategory_id" class="form-input full-width">
      <option value="">Selecione categoria primeiro</option>
    </select>
  </div>
  
  <div>
    <label class="block text-sm font-medium mb-1">Valor</label>
    <input type="number" name="valor" step="0.01" required 
           class="form-input full-width">
  </div>
  
  <div>
    <label class="block text-sm font-medium mb-1">Data</label>
    <input type="date" name="data" required 
           class="form-input full-width">
  </div>
  
  <button type="submit" 
          hx-disabled-elt="this"
          class="btn btn-primary full-width">
    Criar Transação
  </button>
</form>
```

## 4. Inline Edit View

```python
class TransactionEditInlineView(View):
    """Edit transaction inline"""
    template_name = 'transactions/transaction-item.html'
    
    def put(self, request, pk):
        transaction = get_object_or_404(Transaction, id=pk, user=request.user)
        
        # Parse JSON or form data
        import json
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        # Update fields
        transaction.valor = data.get('valor', transaction.valor)
        transaction.descricao = data.get('descricao', transaction.descricao)
        transaction.data = data.get('data', transaction.data)
        transaction.save()
        
        context = {'transaction': transaction}
        return render(request, self.template_name, context)
```

## 5. Delete Confirmation + Action

```python
class TransactionDeleteView(View):
    """Delete with HTMX confirmation"""
    
    def delete(self, request, pk):
        transaction = get_object_or_404(Transaction, id=pk, user=request.user)
        transaction.delete()
        
        # Return empty (HTMX will remove the element)
        return HttpResponse('')
```

**HTML Template** (`transactions/transaction-item.html`):

```html
<tr id="transaction-{{ transaction.id }}" 
    class="border-b hover:bg-gray-50">
  <td class="px-4 py-3">{{ transaction.descricao }}</td>
  <td class="px-4 py-3">{{ transaction.categoria.nome }}</td>
  <td class="px-4 py-3 text-right font-semibold">{{ transaction.valor }}</td>
  <td class="px-4 py-3 text-sm text-gray-500">{{ transaction.data }}</td>
  
  <td class="px-4 py-3 text-right space-x-2">
    <!-- Edit button -->
    <button hx-get="{% url 'transactions:edit' transaction.id %}"
            hx-target="#transaction-{{ transaction.id }}"
            hx-swap="outerHTML"
            class="btn btn-sm btn-secondary">
      Editar
    </button>
    
    <!-- Delete button with confirmation -->
    <button hx-delete="{% url 'transactions:delete' transaction.id %}"
            hx-confirm="Deletar transação?"
            hx-target="#transaction-{{ transaction.id }}"
            hx-swap="outerHTML swap:1s"
            class="btn btn-sm btn-danger">
      Deletar
    </button>
  </td>
</tr>
```

## 6. URLs Configuration

```python
# urls.py
from django.urls import path
from .views import (
    TransactionFilterView,
    TransactionSearchView,
    SubcategoryView,
    TransactionEditInlineView,
    TransactionDeleteView,
)

app_name = 'transactions'

urlpatterns = [
    # HTMX endpoints
    path('filter/', TransactionFilterView.as_view(), name='filter'),
    path('search/', TransactionSearchView.as_view(), name='search'),
    path('api/subcategories/', SubcategoryView.as_view(), name='subcategories'),
    path('api/<int:pk>/edit/', TransactionEditInlineView.as_view(), name='edit'),
    path('api/<int:pk>/delete/', TransactionDeleteView.as_view(), name='delete'),
]
```

## Resposta Esperada

Cada view retorna **apenas o HTML parcial**, não a página completa:

✅ Certo:
```html
<!-- Apenas items da lista -->
<div class="transaction-item">...</div>
<div class="transaction-item">...</div>

<!-- Ou apenas o select -->
<option value="1">Salário</option>
<option value="2">Freelance</option>
```

❌ Errado:
```html
<!DOCTYPE html>
<html>
  <body>
    ... página completa ...
  </body>
</html>
```

## Testing HTMX Views

```python
# test_htmx_views.py
from django.test import TestCase, Client

class HTMXFilterTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # ... create test user and transactions ...
    
    def test_filter_by_category(self):
        response = self.client.get('/transactions/filter/', {
            'category': 1,
        })
        
        # Should return partial HTML (not full page)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'transaction-item')
        self.assertNotContains(response, '<!DOCTYPE html>')
```
