---
name: django-patterns
description: 'Django development standards using CBV, PEP08, and custom admin. Use when: creating Django views, building admin interfaces, or setting up new Django applications.'
argument-hint: 'Leave empty or specify: "views", "admin", "pep08", "setup"'
---

# Django Development Patterns

Padrões de desenvolvimento padronizados para projetos Django, focado em Class-Based Views, conformidade com PEP08 e administração customizada.

## Princípios

- **Apenas Django**: Sem Django REST Framework
- **CBV First**: Usar Class-Based Views para todas as views
- **PEP08 Strict**: Código Python segue PEP08
- **No Django Admin**: Admin padrão não é usado; criar interface customizada
- **Styled Admin**: Painel admin com styling próprio (HTML/CSS/JS)
- **Formatação Django**: Usar extensão de formatação Django para VS Code

## Quando Usar Esta Skill

1. **Criar novas views**: Implementar views usando padrão de CBV com mixins
2. **Setup admin**: Estruturar painel admin customizado
3. **Refatorar código**: Aplicar PEP08 e padrões de CBV
4. **Nova aplicação Django**: Inicializar estrutura base com padrões

## Procedimento Rápido

### 1. Criar Views com CBV

Usar [modelo de CBV com mixins](./assets/cbv-template.py):
- Herdar de mixins customizados
- Implementar `get_context_data()` para lógica de apresentação
- Seguir convenção de nomenclatura

```python
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MyModel
from .forms import MyModelForm

class MyModelListView(LoginRequiredMixin, ListView):
    model = MyModel
    template_name = 'myapp/mymodel_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return MyModel.objects.filter(user=self.request.user)
```

### 2. Configurar Admin Customizado

Criar:
- `urls.py` na app admin customizada
- Views de admin sem herdar de Django Admin
- Templates estilizados (HTML/CSS/JS próprio)
- Sistema de permissões próprio

Referência: [estrutura admin](./assets/admin-structure.md)

### 3. Conformidade PEP08

- **Linhas**: máximo 79 caracteres
- **Imports**: organizar em grupos (stdlib, third-party, local)
- **Nomes**: `snake_case` para funções/variáveis, `PascalCase` para classes
- **Espaçamento**: 2 linhas antes de definições de classe, 1 linha antes de métodos
- **Extensão VS Code**: "Django" (com suporte a formatação automática)

### 4. Estrutura de Aplicação

```
myapp/
├── __init__.py
├── admin.py           # Views de admin customizadas
├── apps.py
├── forms.py
├── models.py
├── urls.py
├── views.py           # CBV apenas
└── templates/
    └── myapp/
```

## Exemplos de Padrões

| Caso | Padrão | Referência |
|------|--------|-----------|
| Listar com paginação | `ListView + LoginRequiredMixin` | [cbv-template.py](./assets/cbv-template.py) |
| Criar com validação | `CreateView + FormValidationMixin` | [cbv-template.py](./assets/cbv-template.py) |
| Admin CRUD | Views customizadas | [admin-structure.md](./assets/admin-structure.md) |
| Permissões | Mixins de permissão próprios | [cbv-template.py](./assets/cbv-template.py) |

## Checklist de Qualidade

- [ ] Todas as views usam CBV
- [ ] Código segue PEP08 (79 chars, imports organizados)
- [ ] Django Admin não é acessado diretamente
- [ ] Painel admin usa styling customizado
- [ ] Testes cobrem as views
- [ ] Formas são validadas tanto no cliente quanto servidor

## Recursos

- [PEP 8 Style Guide](https://pep8.org/)
- [Django CBV Documentation](https://docs.djangoproject.com/en/stable/ref/class-based-views/)
- [Django Mixins Patterns](https://docs.djangoproject.com/en/stable/topics/class-based-views/mixins/)
