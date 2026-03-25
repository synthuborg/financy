# Admin Customizado - Estrutura

## Visão Geral

Criar um painel de administração customizado **sem usar Django Admin**, implementado com views CBV próprias, templates HTML/CSS/JS e sistema de permissões customizado.

## Estrutura de Pastas

```
admin_app/
├── __init__.py
├── apps.py
├── views.py           # Views CBV do painel admin
├── forms.py           # Formulários para admin
├── models.py          # Modelos se necessário
├── urls.py            # URLs do painel admin
├── permissions.py     # Sistema de permissões
├── decorators.py      # Decoradores de autenticação
├── static/
│   ├── css/
│   │   ├── base.css
│   │   └── admin.css
│   └── js/
│       └── admin.js
└── templates/
    └── admin/
        ├── base.html             # Template base
        ├── login.html
        ├── dashboard.html
        └── resources/           # Por modelo
            ├── expense_list.html
            ├── expense_form.html
            ├── user_list.html
            └── user_form.html
```

## Views Customizadas

### 1. Login do Admin

```python
# admin_app/views.py
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

class AdminLoginView(FormView):
    template_name = 'admin/login.html'
    form_class = AdminLoginForm
    
    def form_valid(self, form):
        user = form.cleaned_data['user']
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('admin:dashboard')
```

### 2. Dashboard Principal

```python
class AdminDashboardView(LoginRequiredMixin, AdminPermissionMixin, TemplateView):
    """
    Painel principal do admin com estatísticas e atalhos.
    """
    template_name = 'admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total_users': User.objects.count(),
            'total_expenses': Expense.objects.count(),
            'recent_activity': Activity.objects.all()[:10],
        }
        return context
```

### 3. CRUD Genérico para Admin

```python
class AdminModelListView(LoginRequiredMixin, AdminPermissionMixin, ListView):
    """
    Lista genérica de modelos com filtros e busca.
    """
    template_name = 'admin/resources/model_list.html'
    paginate_by = 50
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name_plural
        context['model_fields'] = [f.name for f in self.model._meta.fields]
        return context


class AdminModelCreateView(LoginRequiredMixin, AdminPermissionMixin, CreateView):
    """
    Criar novo modelo.
    """
    template_name = 'admin/resources/model_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Criar'
        return context


class AdminModelUpdateView(LoginRequiredMixin, AdminPermissionMixin, UpdateView):
    """
    Editar modelo existente.
    """
    template_name = 'admin/resources/model_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        return context


class AdminModelDeleteView(LoginRequiredMixin, AdminPermissionMixin, DeleteView):
    """
    Deletar modelo com confirmação.
    """
    template_name = 'admin/resources/model_confirm_delete.html'
```

## URLs do Admin

```python
# admin_app/urls.py
from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    # Auth
    path('login/', views.AdminLoginView.as_view(), name='login'),
    path('logout/', views.AdminLogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', views.AdminDashboardView.as_view(), name='dashboard'),
    
    # Despesas
    path('expenses/', views.AdminExpenseListView.as_view(), name='expense-list'),
    path('expenses/criar/', views.AdminExpenseCreateView.as_view(), 
         name='expense-create'),
    path('expenses/<int:pk>/editar/', views.AdminExpenseUpdateView.as_view(), 
         name='expense-update'),
    path('expenses/<int:pk>/deletar/', views.AdminExpenseDeleteView.as_view(), 
         name='expense-delete'),
    
    # Usuários
    path('users/', views.AdminUserListView.as_view(), name='user-list'),
    path('users/<int:pk>/editar/', views.AdminUserUpdateView.as_view(), 
         name='user-update'),
    path('users/<int:pk>/deletar/', views.AdminUserDeleteView.as_view(), 
         name='user-delete'),
]
```

## Sistema de Permissões

```python
# admin_app/permissions.py
from functools import wraps
from django.http import HttpResponseForbidden

def admin_required(view_func):
    """Decorador para verificar se é admin."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'admin_profile'):
            return HttpResponseForbidden('Acesso negado')
        return view_func(request, *args, **kwargs)
    return wrapper


# Mixin para views CBV
from django.contrib.auth.mixins import UserPassesTestMixin

class AdminPermissionMixin(UserPassesTestMixin):
    """Verifica se usuário tem permissão de admin."""
    
    def test_func(self):
        return hasattr(self.request.user, 'admin_profile')
    
    def handle_no_permission(self):
        return HttpResponseForbidden('Acesso negado')
```

## Template Base

```html
<!-- admin_app/templates/admin/base.html -->
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Admin{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/admin.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <div class="admin-wrapper">
        <!-- Sidebar -->
        <aside class="admin-sidebar">
            <div class="admin-logo">
                <h2>Admin Panel</h2>
            </div>
            <nav class="admin-nav">
                <ul>
                    <li><a href="{% url 'admin:dashboard' %}">Dashboard</a></li>
                    <li><a href="{% url 'admin:expense-list' %}">Despesas</a></li>
                    <li><a href="{% url 'admin:user-list' %}">Usuários</a></li>
                    <li><a href="{% url 'admin:logout' %}">Logout</a></li>
                </ul>
            </nav>
        </aside>
        
        <!-- Main Content -->
        <main class="admin-main">
            <header class="admin-header">
                <h1>{% block page_title %}{% endblock %}</h1>
            </header>
            
            <section class="admin-content">
                {% if messages %}
                    <div class="messages">
                        {% for message in messages %}
                            <div class="alert alert-{{ message.tags }}">
                                {{ message }}
                            </div>
                        {% endfor %}
                    </div>
                {% endif %}
                
                {% block content %}{% endblock %}
            </section>
        </main>
    </div>
    
    <script src="{% static 'js/admin.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

## CSS Básico

```css
/* admin_app/static/css/admin.css */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
                 Ubuntu, Cantarell, sans-serif;
    background-color: #f5f5f5;
}

.admin-wrapper {
    display: flex;
    min-height: 100vh;
}

.admin-sidebar {
    width: 250px;
    background-color: #2c3e50;
    color: white;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
}

.admin-logo h2 {
    margin-bottom: 30px;
    font-size: 1.5em;
}

.admin-nav ul {
    list-style: none;
}

.admin-nav li {
    margin-bottom: 10px;
}

.admin-nav a {
    color: #ecf0f1;
    text-decoration: none;
    display: block;
    padding: 10px 15px;
    border-radius: 4px;
    transition: background-color 0.2s;
}

.admin-nav a:hover {
    background-color: #34495e;
}

.admin-main {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.admin-header {
    background-color: white;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.admin-header h1 {
    color: #2c3e50;
    font-size: 2em;
}

.admin-content {
    flex: 1;
    padding: 20px;
}

/* Table Styles */
table {
    width: 100%;
    background-color: white;
    border-collapse: collapse;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border-radius: 4px;
    overflow: hidden;
}

th {
    background-color: #34495e;
    color: white;
    padding: 15px;
    text-align: left;
    font-weight: 600;
}

td {
    padding: 12px 15px;
    border-bottom: 1px solid #ecf0f1;
}

tr:hover {
    background-color: #f9f9f9;
}

/* Button Styles */
.btn {
    display: inline-block;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1em;
    text-decoration: none;
    transition: all 0.2s;
}

.btn-primary {
    background-color: #3498db;
    color: white;
}

.btn-primary:hover {
    background-color: #2980b9;
}

.btn-danger {
    background-color: #e74c3c;
    color: white;
}

.btn-danger:hover {
    background-color: #c0392b;
}

.btn-secondary {
    background-color: #95a5a6;
    color: white;
}

.btn-secondary:hover {
    background-color: #7f8c8d;
}

/* Messages */
.messages {
    margin-bottom: 20px;
}

.alert {
    padding: 15px;
    margin-bottom: 10px;
    border-radius: 4px;
    border-left: 4px solid;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
    border-color: #28a745;
}

.alert-error, .alert-danger {
    background-color: #f8d7da;
    color: #721c24;
    border-color: #f5c6cb;
}

.alert-info {
    background-color: #d1ecf1;
    color: #0c5460;
    border-color: #bee5eb;
}
```

## Integração no Django

### settings.py

```python
INSTALLED_APPS = [
    # ...
    'admin_app',
    # ...
]

# URLs do admin customizado
ADMIN_URL = '/admin/'  # Customizar como preferir
```

### urls.py (projeto)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Desabilitar Django Admin se desejar
    # path('admin/', admin.site.urls),
    
    # Admin customizado
    path('admin/', include('admin_app.urls')),
    
    # Outras urls
]
```

## Checklist de Implementação

- [ ] App `admin_app` criada
- [ ] Views CBV para CRUD
- [ ] Mixins de permissão implementados
- [ ] URLs estruturadas
- [ ] Templates base e recursos
- [ ] CSS/JS para styling
- [ ] Sistema de autenticação
- [ ] Testes das permissões
- [ ] Documentação de acesso
