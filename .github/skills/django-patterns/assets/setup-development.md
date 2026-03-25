# Setup de Desenvolvimento Django

## Extensões VS Code Recomendadas

### Obrigatórias

1. **Python** (Microsoft)
   - ID: `ms-python.python`
   - Fornece intellisense, debugging, formatação Python

2. **Django** (Baptiste Darthenay)
   - ID: `batisteo.vscode-django`
   - Syntax highlight, snippets e formatação Django

3. **Pylance** (Microsoft)
   - ID: `ms-python.vscode-pylance`
   - Type checking, intellisense avançado

### Recomendadas

4. **Black Formatter** (Microsoft)
   - ID: `ms-python.black-formatter`
   - Formatação automática PEP08

5. **isort** (Microsoft)
   - ID: `ms-python.isort`
   - Organização automática de imports

6. **Pylint** (Microsoft)
   - ID: `ms-python.pylint`
   - Linting e análise estática

## Configuração VS Code

Adicione ao `.vscode/settings.json`:

```json
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--load-plugins=pylint_django",
        "--django-settings-module=config.settings"
    ],
    "isort.args": ["--profile", "black"],
    "black-formatter.args": ["--line-length=79"],
    "[django-html]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    }
}
```

## Arquivo `.pylintrc`

Criar na raiz do projeto:

```ini
[MASTER]
django-settings-module=config.settings
load-plugins=pylint_django

[MESSAGES CONTROL]
disable=
    missing-docstring,
    too-few-public-methods,

[FORMAT]
max-line-length=79

[DESIGN]
max-attributes=7
```

## Arquivo `pyproject.toml`

```toml
[tool.black]
line-length = 79
target-version = ['py39', 'py310', 'py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # diretórios
  migrations
  | __pycache__
  | \.eggs
  | \.git
  | build
  | dist
  | venv
)/
'''

[tool.isort]
profile = "black"
line_length = 79
multi_line_mode = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
skip_glob = ["*/migrations/*"]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings"
python_files = ["tests.py", "test_*.py", "*_tests.py"]
addopts = "--cov=. --cov-report=html --strict-markers"

[tool.coverage.run]
omit = [
    "*/migrations/*",
    "*/tests/*",
    "manage.py",
    "setup.py",
]
```

## PEP08 - Regras Principais

### Indentação e Espaçamento

```python
# ✓ Correto
def funcao_descritivo_e_longo(parametro1, parametro2,
                               parametro3, parametro4):
    if parametro1:
        resultado = (parametro1 + parametro2 +
                     parametro3 + parametro4)
    return resultado


# ✗ Incorreto
def funcao(p1,p2,p3):
    if p1:result = p1+p2; return result
```

### Imports

```python
# ✓ Correto - Organizado em 3 grupos
import os
import sys
from pathlib import Path

import django
from django.conf import settings

from myapp.models import User
from myapp.utils import helper_function


# ✗ Incorreto - Desorganizado
from django.conf import settings
import os
from myapp.models import User
import sys
```

### Nomes

```python
# ✓ Correto
def calcular_total_despesas(user_id):
    pass

class ContaBancaria:
    def __init__(self, numero_conta):
        self.numero_conta = numero_conta
        self._saldo = 0.0  # Privado
        self.__pin = None  # Muito privado

TAXA_JUROS = 0.05
DIAS_PADRAO = 30


# ✗ Incorreto
def CalcularTotal(UserID):  # CamelCase funções
    pass

class contaBancaria:  # lowercase classes
    pass

taxajuros = 0.05  # lowercase constantes
```

### Comprimento de Linha

```python
# ✓ Correto - 79 caracteres máximo
resultado = (
    funcao_longa_com_muitos_parametros(
        arg1, arg2, arg3,
        arg4, arg5, arg6
    )
)


# ✗ Incorreto - Linha muito longa
resultado = funcao_longa_com_muitos_parametros(arg1, arg2, arg3, arg4, arg5, arg6)
```

### Whitespace

```python
# ✓ Correto
x = 1
y = 2
z = x + y

lista = [1, 2, 3]
dicionario = {'chave': 'valor'}

def funcao(argumento=valor_padrao):
    pass


# ✗ Incorreto
x=1
y=2
z=x+y

lista=[1,2,3]
dicionario={'chave':'valor'}

def funcao(argumento = valor_padrao):
    pass
```

### Boas Práticas

```python
# ✓ Correto
class MyModelListView(LoginRequiredMixin, ListView):
    """Descrição breve em uma linha."""
    
    model = MyModel
    paginate_by = 20
    
    def get_queryset(self):
        """Retorna apenas objetos do usuário atual."""
        return self.model.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        return context


# ✗ Incorreto
class MyModelListView(LoginRequiredMixin,ListView):
    model=MyModel;paginate_by=20
    def get_queryset(self):return self.model.objects.filter(user=self.request.user)
```

## Desenvolvimento Seguro

### Variáveis de Ambiente

```python
# settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Usar python-dotenv
from dotenv import load_dotenv

load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-insecure-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
```

### .env (exemplo)

```
SECRET_KEY=sua-chave-segura-aqui
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

## Verificando Qualidade

### Linha de Comando

```bash
# Verificar PEP08 com flake8
flake8 myapp/

# Formatar automaticamente
black myapp/

# Organizar imports
isort myapp/

# Verificar tipos
mypy myapp/

# Executar linter
pylint myapp/
```

### Pre-commit Hook

Arquivo `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Formatar código antes de commit

black .
isort .
pylint myapp/
```

## Estrutura Base do Projeto

```
hackaton_app_financas/
├── .github/
│   └── skills/
│       └── django-patterns/
├── .vscode/
│   └── settings.json
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── myapp/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── .env
├── .env.example
├── .gitignore
├── .pylintrc
├── pyproject.toml
├── manage.py
└── requirements.txt
```

## Próximos Passos

1. Instalar extensões recomendadas
2. Configurar `.vscode/settings.json`
3. Criar `pyproject.toml` e `.pylintrc`
4. Instalar dependências: `pip install black isort pylint pylint-django`
5. Executar `black .` e `isort .` para formatar código existente
6. Começar novo desenvolvimento seguindo padrões
