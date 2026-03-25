---
name: new-feature
description: End-to-end workflow for adding new features to hackaton_app_financas after project is live. Plan → implement → review → test → commit. Uses all project skills together.
instructions: |
  Use this skill when adding any new feature to the project after initial launch.
  Follow the full lifecycle: plan → implement → review → test → commit.
  Always use existing project skills for each phase (django-patterns, htmx-patterns, etc.).
keywords: [feature, new-feature, workflow, post-launch, planning, implementation, deploy]
---

# New Feature Workflow — hackaton_app_financas

Fluxo completo para adicionar features ao projeto já finalizado, sem quebrar o que funciona.

---

## Fluxo em 6 Etapas

```
1. 📋 Planejar    → Definir escopo, impacto, decisões técnicas
2. 🏗️ Preparar   → Sincronizar com main, criar estrutura
3. 💻 Implementar → Código seguindo padrões do projeto
4. 🔍 Revisar    → Code review antes de subir
5. 🧪 Testar     → Testes antes de produção
6. 🚀 Subir      → Commit + push com mensagem clara
```

---

## Etapa 1 — Planejar

Antes de codar, responder estas perguntas:

### Definição da Feature

```
Nome da feature: ___________________________________
Objetivo: O que o usuário consegue fazer com isso?
___________________________________________________

Tipo:
[ ] Nova página / rota
[ ] Novo model + migração
[ ] Componente de UI (chart, card, modal)
[ ] Melhoria de performance

Onde entra no projeto?
[ ] Dashboard principal
[ ] Tela de transações
[ ] Tela de categorias
[ ] Outra: ________________
```

### Análise de Impacto (o que pode quebrar?)

```
Models afetados:        ___________________________
Views afetadas:         ___________________________
Templates afetados:     ___________________________
URLs adicionadas/mudadas: _________________________
Migrations necessárias: [ ] Sim  [ ] Não
```

### Decisões Técnicas

Escolha antes de começar:

| Decisão | Opções | Escolha |
|---------|--------|---------|
| View type | CBV (recomendado) / FBV | |
| Interatividade | HTMX / reload de página | |
| Dados novos? | Novo model / campo existente | |
| Layout | Página nova / componente inline | |

---

## Etapa 2 — Preparar

### Sincronizar com main

```bash
git pull origin main
git status   # garantir que está limpo
```

### Verificar estado do projeto

```bash
python manage.py check          # checar erros Django
python manage.py showmigrations # ver estado das migrations
```

### Estrutura de arquivos a criar/editar

**Para nova página:**
```
apps/<app>/
├── views.py          ← adicionar nova view
├── urls.py           ← adicionar nova URL
models.py             ← se tiver novo model
templates/<app>/
└── nova-pagina.html  ← criar template
```

**Para novo model:**
```
apps/<app>/models.py            ← definir model
apps/<app>/migrations/          ← gerada automaticamente
apps/<app>/views.py             ← views CRUD
templates/<app>/                ← templates
```

**Para componente de UI:**
```
templates/components/
└── novo-componente.html        ← componente reutilizável
```

---

## Etapa 3 — Implementar

### 3a. Novo Model (se necessário)

Seguir @django-patterns:

```python
# apps/<app>/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class NewFeatureModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='new_features',
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
```

Gerar migration:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3b. Nova View CBV

Seguir @django-patterns (CBV + LoginRequiredMixin):

```python
# apps/<app>/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import NewFeatureModel


class NewFeatureListView(LoginRequiredMixin, ListView):
    model = NewFeatureModel
    template_name = '<app>/new-feature-list.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return NewFeatureModel.objects.filter(user=self.request.user)


class NewFeatureCreateView(LoginRequiredMixin, CreateView):
    model = NewFeatureModel
    fields = ['name']
    template_name = '<app>/new-feature-form.html'
    success_url = reverse_lazy('<app>:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
```

### 3c. URL

```python
# apps/<app>/urls.py
from django.urls import path
from .views import NewFeatureListView, NewFeatureCreateView

app_name = '<app>'
urlpatterns = [
    path('new-feature/', NewFeatureListView.as_view(), name='list'),
    path('new-feature/create/', NewFeatureCreateView.as_view(), name='create'),
]
```

### 3d. Template

Seguir @frontend-finance-design (mobile-first, Tailwind):

```html
{% extends "base.html" %}

{% block title %}Nova Feature | Financeiro{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-6">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-gray-900">Nome da Feature</h1>
    <a href="{% url '<app>:create' %}"
       class="btn btn-primary">
      + Adicionar
    </a>
  </div>

  {% for item in items %}
    <div class="bg-white rounded-lg shadow-sm border p-4 mb-3">
      <p class="font-semibold">{{ item.name }}</p>
    </div>
  {% empty %}
    <p class="text-center text-gray-500 py-8">
      Nenhum item ainda. Adicione o primeiro!
    </p>
  {% endfor %}
</div>
{% endblock %}
```

### 3e. Interatividade com HTMX

Seguir @htmx-patterns (sem JS customizado):

```html
<!-- Filtro sem reload -->
<button hx-get="{% url '<app>:list' %}"
        hx-vals='{"filter": "value"}'
        hx-target="#list"
        hx-swap="innerHTML">
  Filtrar
</button>

<!-- Form sem redirect -->
<form hx-post="{% url '<app>:create' %}"
      hx-target="#list"
      hx-swap="beforeend">
  {% csrf_token %}
  <input name="name" required>
  <button type="submit">Adicionar</button>
</form>
```

### 3f. Performance (se necessário)

```python
# Evitar N+1 queries
queryset = NewFeatureModel.objects.filter(
    user=request.user
).select_related('categoria').prefetch_related('tags')

# Cache para dados que não mudam (ex: categorias)
from django.core.cache import cache

def get_categories(user_id):
    key = f'categories_{user_id}'
    categories = cache.get(key)
    if categories is None:
        categories = list(Category.objects.filter(user_id=user_id))
        cache.set(key, categories, timeout=300)  # 5 min
    return categories
```

---

## Etapa 4 — Revisar (@code-review)

Antes de commitar, passar pelo checklist do @code-review:

```
[ ] Sem código duplicado (DRY)
[ ] Sem imports não usados
[ ] Ownership check em todas as queries (filter(user=request.user))
[ ] Sem hardcoded credentials
[ ] PEP08: snake_case, linhas ≤ 79 chars
[ ] Templates: texto em PT, sem lógica complexa
[ ] HTMX: sem onclick/onchange misturado
[ ] Nomes em EN no código, PT no template
```

Pedir review completo:
```
@code-review Revise o código desta nova feature: [colar código]
```

---

## Etapa 5 — Testar (@testing-workflow)

### Smoke Test Manual (mínimo obrigatório)

```
[ ] Abrir a nova página no browser
[ ] Criar um item → aparece na lista?
[ ] Editar → salva corretamente?
[ ] Deletar → some da lista?
[ ] Testar em mobile (DevTools → toggle device)
[ ] Testar sem estar logado → redireciona para /login/?
[ ] Testar com outro usuário → não vê dados do primeiro?
```

### Teste Playwright (se der tempo)

Seguir @testing-workflow:

```typescript
test('new feature: create and list item', async ({ page }) => {
  await page.goto('/new-feature/');
  
  // Criar item
  await page.click('a[href*="create"]');
  await page.fill('input[name="name"]', 'Teste item');
  await page.click('button[type="submit"]');
  
  // Verificar na lista
  await expect(page.locator('text=Teste item')).toBeVisible();
});
```

### Verificar que não quebrou nada (regression)

```bash
python manage.py check           # sem erros Django
python manage.py test            # testes existentes passam
```

---

## Etapa 6 — Subir (@git-workflow)

### Commit

```bash
git pull origin main             # sincronizar antes de pushear
git add .
git status                       # confirmar o que vai subir
git commit -m "feat: add <feature-name>"
git push origin main
```

### Formato do commit

```
feat: add <descrição da feature em inglês>
```

Exemplos:
```bash
git commit -m "feat: add budget goals tracker"
git commit -m "feat: add monthly expense chart"
git commit -m "feat: add CSV export for transactions"
git commit -m "feat: add notification for budget limit"
```

---

## Checklist Completo (antes de dar como pronto)

### Planejamento
- [ ] Escopo definido (o que faz e o que não faz)
- [ ] Impacto mapeado (models, views, templates afetados)
- [ ] Decisões técnicas tomadas (CBV? HTMX? Novo model?)

### Implementação
- [ ] Model criado e migrado (se necessário)
- [ ] View CBV com `LoginRequiredMixin`
- [ ] `filter(user=request.user)` em todas as queries
- [ ] URL registrada no `urls.py`
- [ ] Template mobile-first com Tailwind
- [ ] HTMX para interações (sem onclick)
- [ ] Texto do usuário em Português
- [ ] Nomes de código em Inglês

### Qualidade
- [ ] @code-review passou
- [ ] Smoke test manual feito
- [ ] Não quebrou outras telas
- [ ] `python manage.py check` sem erros

### Deploy
- [ ] `git pull` antes de pushear
- [ ] Commit no formato `feat: ...`
- [ ] Push feito com sucesso
- [ ] Verificar no servidor/produção que funciona

---

## Tipos de Feature — Atalhos

### Nova Página Completa

```
1. Model → Migration → View CBV → URL → Template
2. Usar @django-patterns para estrutura
3. Usar @frontend-finance-design para layout
4. Usar @htmx-patterns para filtros/busca
```

### Novo Componente de UI (sem model)

```
1. Criar template em templates/components/
2. Usar {% include %} onde necessário
3. Usar @frontend-finance-design para Tailwind
4. Usar @htmx-patterns se tiver interatividade
```

### Melhoria de Performance

```
1. Identificar query lenta (Django Debug Toolbar ou prints)
2. Adicionar select_related / prefetch_related
3. Adicionar cache se dado não muda frequentemente
4. Medir antes e depois
```

---

## Skills Utilizadas neste Workflow

| Fase | Skill |
|------|-------|
| Implementar views/models | @django-patterns |
| Implementar interações | @htmx-patterns |
| Implementar layout | @frontend-finance-design |
| Revisar código | @code-review |
| Revisar textos | @writing-standards |
| Testar | @testing-workflow |
| Commitar e subir | @git-workflow |
