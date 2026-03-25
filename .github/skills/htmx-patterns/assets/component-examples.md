# Component Examples - Componentes Práticos

Exemplos prontos para copiar e adaptar ao projeto.

## 1. Filter Buttons Component

**HTML:**

```html
{% comment %} transactions/components/filter-buttons.html {% endcomment %}
<div class="filter-buttons flex gap-2 mb-6 overflow-x-auto pb-2">
  <!-- "All" button -->
  <button hx-get="{% url 'transactions:filter' %}"
          hx-target="#transaction-list"
          hx-swap="innerHTML"
          hx-indicator="#loading"
          class="btn btn-sm btn-secondary whitespace-nowrap">
    Todas
  </button>
  
  <!-- Category buttons -->
  {% for category in categories %}
    <button hx-get="{% url 'transactions:filter' %}"
            hx-vals='{"category": {{ category.id }} }'
            hx-target="#transaction-list"
            hx-swap="innerHTML"
            hx-indicator="#loading"
            class="btn btn-sm btn-secondary whitespace-nowrap
                   {% if selected_category == category.id %}btn-primary{% endif %}">
      {{ category.nome }}
    </button>
  {% endfor %}
</div>

<!-- Loading indicator -->
<div id="loading" class="htmx-indicator flex items-center gap-2 text-blue-600">
  <div class="spinner-border animate-spin inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full"></div>
  <span class="text-sm">Carregando...</span>
</div>

<!-- Transaction list container -->
<div id="transaction-list">
  {% include "transactions/components/transaction-list.html" %}
</div>
```

---

## 2. Live Search Component

**HTML:**

```html
{% comment %} transactions/components/live-search.html {% endcomment %}
<div class="relative mb-4">
  <input type="text"
         placeholder="🔍 Buscar transações (descrição ou categoria)..."
         hx-get="{% url 'transactions:search' %}"
         hx-trigger="keyup changed delay:300ms"
         hx-target="#search-dropdown"
         hx-select="#search-dropdown"
         name="q"
         value="{{ query }}"
         class="form-input full-width"
         autocomplete="off">
  
  <!-- Search results dropdown -->
  <div id="search-dropdown" class="search-dropdown hidden absolute top-full left-0 right-0 
                                   bg-white border border-gray-300 rounded-lg shadow-lg 
                                   z-50 mt-1 max-h-96 overflow-y-auto">
    {% comment %} Results render here {% endcomment %}
  </div>
</div>

{% comment %} CSS to show dropdown {% endcomment %}
<style>
  #search-dropdown:not(.empty) {
    display: block;
  }
  
  .search-dropdown.empty {
    display: none;
  }
</style>
```

**View (Django):**

```python
# transactions/views.py
class TransactionSearchView(View):
    def get(self, request):
        q = request.GET.get('q', '').strip()
        
        if len(q) < 2:
            return render(request, 'transactions/components/search-results.html', {
                'results': [],
            })
        
        from django.db.models import Q
        results = Transaction.objects.filter(
            user=request.user
        ).filter(
            Q(descricao__icontains=q) | 
            Q(categoria__nome__icontains=q)
        )[:10]
        
        return render(request, 'transactions/components/search-results.html', {
            'results': results,
        })
```

**Results Template:**

```html
{% comment %} transactions/components/search-results.html {% endcomment %}
<div id="search-dropdown" class="{% if not results %}empty{% endif %}">
  {% if results %}
    <ul>
      {% for result in results %}
        <li class="border-b last:border-b-0 hover:bg-blue-50 cursor-pointer
                   transition-colors"
            hx-on::click="htmx.ajax('GET', '{% url 'transactions:detail' result.id %}', 
                                    {target: '#main'})">
          <a class="block px-4 py-3">
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <span class="font-semibold text-gray-900">{{ result.descricao }}</span>
                <span class="text-gray-500 text-sm ml-2">{{ result.categoria.nome }}</span>
              </div>
              <span class="font-semibold whitespace-nowrap ml-2
                           {% if result.tipo == 'entrada' %}text-green-600{% else %}text-red-600{% endif %}">
                {{ result.valor|floatformat:2 }}
              </span>
            </div>
            <p class="text-xs text-gray-400 mt-1">{{ result.data|date:"d/m/Y" }}</p>
          </a>
        </li>
      {% endfor %}
    </ul>
  {% elif query %}
    <div class="px-4 py-3 text-center text-gray-500">
      Nenhum resultado para "{{ query }}"
    </div>
  {% endif %}
</div>
```

---

## 3. Dynamic Form (Dependent Selects)

**HTML:**

```html
{% comment %} transactions/components/form.html {% endcomment %}
<form hx-post="{% url 'transactions:create' %}"
      hx-target="#form-message"
      hx-swap="innerHTML"
      class="space-y-4 max-w-md">
  {% csrf_token %}
  
  <!-- Type (entrada/saída) -->
  <div>
    <label class="block text-sm font-semibold mb-2 text-gray-700">Tipo</label>
    <div class="flex gap-4">
      <label class="flex items-center">
        <input type="radio" name="tipo" value="entrada" required 
               class="w-4 h-4 accent-green-600">
        <span class="ml-2">Entrada</span>
      </label>
      <label class="flex items-center">
        <input type="radio" name="tipo" value="saida" 
               class="w-4 h-4 accent-red-600">
        <span class="ml-2">Saída</span>
      </label>
    </div>
  </div>
  
  <!-- Category (triggers subcategory) -->
  <div>
    <label for="category" class="block text-sm font-semibold mb-2 text-gray-700">
      Categoria
    </label>
    <select id="category" name="category_id" required
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
    <label for="subcategory" class="block text-sm font-semibold mb-2 text-gray-700">
      Subcategoria
    </label>
    <select id="subcategory" name="subcategory_id" 
            class="form-input full-width disabled:bg-gray-100"
            disabled>
      <option value="">Selecione categoria primeiro</option>
    </select>
  </div>
  
  <!-- Amount -->
  <div>
    <label for="amount" class="block text-sm font-semibold mb-2 text-gray-700">
      Valor
    </label>
    <input type="number" id="amount" name="valor" step="0.01" required 
           placeholder="0.00"
           class="form-input full-width">
  </div>
  
  <!-- Description -->
  <div>
    <label for="desc" class="block text-sm font-semibold mb-2 text-gray-700">
      Descrição
    </label>
    <input type="text" id="desc" name="descricao" required 
           placeholder="Ex: Pagamento da conta"
           class="form-input full-width">
  </div>
  
  <!-- Date -->
  <div>
    <label for="date" class="block text-sm font-semibold mb-2 text-gray-700">
      Data
    </label>
    <input type="date" id="date" name="data" required 
           class="form-input full-width">
  </div>
  
  <!-- Submit -->
  <button type="submit" 
          hx-disabled-elt="this"
          class="btn btn-primary full-width">
    Criar Transação
  </button>
  
  <!-- Response message -->
  <div id="form-message"></div>
</form>
```

**Subcategory Template:**

```html
{% comment %} transactions/components/subcategories-select.html {% endcomment %}
<label for="subcategory" class="block text-sm font-semibold mb-2 text-gray-700">
  Subcategoria
</label>
<select id="subcategory" name="subcategory_id" 
        class="form-input full-width">
  <option value="">Selecione...</option>
  {% for sub in subcategories %}
    <option value="{{ sub.id }}">{{ sub.nome }}</option>
  {% endfor %}
</select>
```

---

## 4. Pagination Component

**HTML:**

```html
{% comment %} transactions/components/pagination.html {% endcomment %}
<div class="mt-6 pt-4 border-t border-gray-200">
  {% if page_obj.has_other_pages %}
    <div class="flex justify-between items-center">
      <!-- Previous button -->
      <div>
        {% if page_obj.has_previous %}
          <button hx-get="{% url 'transactions:filter' %}"
                  hx-vals='{"page": {{ page_obj.previous_page_number }} }'
                  hx-target="#transaction-list"
                  hx-swap="innerHTML"
                  hx-indicator="#loading"
                  class="btn btn-sm btn-secondary">
            ← Anterior
          </button>
        {% else %}
          <span class="btn btn-sm btn-secondary opacity-50 cursor-not-allowed">
            ← Anterior
          </span>
        {% endif %}
      </div>
      
      <!-- Page info -->
      <div class="text-sm text-gray-600 font-medium">
        Página <span class="font-bold">{{ page_obj.number }}</span> 
        de <span class="font-bold">{{ page_obj.paginator.num_pages }}</span>
        
        <span class="text-gray-400 ml-2">
          ({{ page_obj.paginator.count }} itens)
        </span>
      </div>
      
      <!-- Next button -->
      <div>
        {% if page_obj.has_next %}
          <button hx-get="{% url 'transactions:filter' %}"
                  hx-vals='{"page": {{ page_obj.next_page_number }} }'
                  hx-target="#transaction-list"
                  hx-swap="innerHTML"
                  hx-indicator="#loading"
                  class="btn btn-sm btn-secondary">
            Próxima →
          </button>
        {% else %}
          <span class="btn btn-sm btn-secondary opacity-50 cursor-not-allowed">
            Próxima →
          </span>
        {% endif %}
      </div>
    </div>
  {% endif %}
</div>
```

---

## 5. Transaction List Item (with inline actions)

**HTML:**

```html
{% comment %} transactions/components/transaction-item.html {% endcomment %}
<tr id="transaction-{{ transaction.id }}" 
    class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
  
  <td class="px-4 py-4">
    <div class="font-semibold text-gray-900">{{ transaction.descricao }}</div>
    <div class="text-sm text-gray-500">{{ transaction.categoria.nome }}</div>
  </td>
  
  <td class="px-4 py-4 text-right">
    <span class="font-bold text-lg {% if transaction.tipo == 'entrada' %}text-green-600{% else %}text-red-600{% endif %}">
      {% if transaction.tipo == 'entrada' %}+{% else %}-{% endif %}
      {{ transaction.valor|floatformat:2 }}
    </span>
  </td>
  
  <td class="px-4 py-4 text-sm text-gray-500 text-right">
    {{ transaction.data|date:"d/m/Y" }}
  </td>
  
  <td class="px-4 py-4 text-right space-x-2 flex justify-end">
    <!-- Edit button -->
    <button hx-get="{% url 'transactions:edit' transaction.id %}"
            hx-target="#transaction-{{ transaction.id }}"
            hx-swap="outerHTML"
            class="btn btn-sm btn-secondary"
            title="Editar">
      ✏️
    </button>
    
    <!-- Delete button -->
    <button hx-delete="{% url 'transactions:delete' transaction.id %}"
            hx-confirm="Tem certeza que deseja deletar esta transação?"
            hx-target="#transaction-{{ transaction.id }}"
            hx-swap="outerHTML swap:0.5s"
            class="btn btn-sm btn-danger"
            title="Deletar">
      🗑️
    </button>
  </td>
</tr>
```

**Transaction List Container:**

```html
{% comment %} transactions/components/transaction-list.html {% endcomment %}
<div class="overflow-x-auto">
  <table class="w-full">
    <thead>
      <tr class="bg-gray-50 border-b-2 border-gray-200">
        <th class="px-4 py-3 text-left font-semibold text-gray-700">
          Descrição
        </th>
        <th class="px-4 py-3 text-right font-semibold text-gray-700">
          Valor
        </th>
        <th class="px-4 py-3 text-right font-semibold text-gray-700">
          Data
        </th>
        <th class="px-4 py-3 text-right font-semibold text-gray-700">
          Ações
        </th>
      </tr>
    </thead>
    <tbody>
      {% for transaction in transactions %}
        {% include "transactions/components/transaction-item.html" %}
      {% empty %}
        <tr>
          <td colspan="4" class="px-4 py-8 text-center text-gray-500">
            Nenhuma transação encontrada.
          </td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</div>

{% include "transactions/components/pagination.html" %}
```

---

## 6. Integrating All Components in Dashboard

**Main Dashboard Template:**

```html
{% comment %} transactions/dashboard.html {% endcomment %}
{% extends "base.html" %}

{% block title %}Transações | Financeiro{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-6">
  <h1 class="text-3xl font-bold mb-8">Transações</h1>
  
  <!-- Loading indicator -->
  <div id="loading" class="htmx-indicator hidden mb-4 flex items-center gap-2 text-blue-600">
    <div class="spinner-border animate-spin inline-block w-5 h-5 border-2 border-current border-t-transparent rounded-full"></div>
    <span>Carregando...</span>
  </div>
  
  <!-- Filter buttons -->
  {% include "transactions/components/filter-buttons.html" %}
  
  <!-- Live search -->
  {% include "transactions/components/live-search.html" %}
  
  <!-- Quick create button -->
  <div class="mb-6">
    <button hx-get="{% url 'transactions:create-form' %}"
            hx-target="#create-modal"
            hx-swap="innerHTML"
            class="btn btn-primary gap-2">
      ➕ Nova Transação
    </button>
  </div>
  
  <!-- Create modal (appears via HTMX) -->
  <div id="create-modal" class="hidden fixed inset-0 bg-black/50 z-40
                               flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-lg max-w-md w-full p-6">
      <h2 class="text-xl font-bold mb-4">Nova Transação</h2>
      {% include "transactions/components/form.html" %}
    </div>
  </div>
  
  <!-- Transaction list (loads via HTMX) -->
  <div id="transaction-list">
    {% include "transactions/components/transaction-list.html" %}
  </div>
</div>

<!-- HTMX script -->
<script src="https://unpkg.com/htmx.org@1.9.10"></script>

{% endblock %}
```

---

## Testing Components

```python
# test_htmx_components.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()

class HTMXComponentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='pass123')
        self.client.login(username='testuser', password='pass123')
    
    def test_filter_component_returns_partial(self):
        """Filter should return HTML partial, not full page"""
        response = self.client.get('/transactions/filter/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'transaction-item')
        self.assertNotContains(response, '<!DOCTYPE')
    
    def test_search_component_returns_partial(self):
        """Search should return results partial"""
        response = self.client.get('/transactions/search/?q=test')
        
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<!DOCTYPE')
    
    def test_pagination_links_use_htmx(self):
        """Pagination links should have hx-* attributes"""
        response = self.client.get('/transactions/filter/')
        
        self.assertContains(response, 'hx-get')
        self.assertContains(response, 'hx-vals')
        self.assertContains(response, 'hx-swap')
```

---

**Integração com:**
- [@django-patterns](link-to-skill:/django-patterns) para estrutura de views CBV
- [@frontend-finance-design](link-to-skill:/frontend-finance-design) para estilos Tailwind
- [@testing-workflow](link-to-skill:/testing-workflow) para testar componentes
