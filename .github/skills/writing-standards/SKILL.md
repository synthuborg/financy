---
name: writing-standards
description: Writing standards for hackaton_app_financas. Enforce correct Portuguese (UI, messages, comments) and English (code, commits, docs). Fix typos, mixed-language naming, accents, and inconsistent terminology.
instructions: |
  Use this skill to review and fix writing errors in any part of the project.
  Enforce the bilingual rule: English for code identifiers, Portuguese for UI-facing text.
  Apply the project glossary for consistent terminology in both languages.
keywords: [writing, português, english, typos, naming, messages, consistency, glossary]
---

# Writing Standards — hackaton_app_financas

**Regra base:** Código em **Inglês**, texto do usuário em **Português**.

---

## Regra de Idioma por Contexto

| Contexto | Idioma | Exemplo |
|----------|--------|---------|
| Nomes de variáveis, funções, classes | 🇺🇸 Inglês | `transaction_value`, `get_balance()` |
| Comentários no código | 🇺🇸 Inglês | `# Calculate monthly balance` |
| Commits e PRs | 🇺🇸 Inglês | `feat: add transaction filter` |
| Mensagens UI (labels, botões, títulos) | 🇧🇷 Português | `Adicionar Transação` |
| Mensagens de erro/sucesso Django | 🇧🇷 Português | `Transação salva com sucesso.` |
| Templates HTML (texto visível) | 🇧🇷 Português | `Saldo atual`, `Filtrar por categoria` |
| Documentação interna (README, docs) | 🇺🇸 Inglês | `## Installation`, `## Usage` |

---

## Erros em Português — Checklist

### 1. Acentuação

```
❌ transacão    → ✅ transação
❌ saida        → ✅ saída
❌ usuario      → ✅ usuário
❌ categorias   → ✅ categorias ✓ (sem acento)
❌ pagina       → ✅ página
❌ periodo      → ✅ período
❌ historico    → ✅ histórico
❌ relatorio    → ✅ relatório
❌ proximo      → ✅ próximo
❌ numero       → ✅ número
```

### 2. Concordância Nominal

```
❌ os transação        → ✅ as transações
❌ uma entrada novo    → ✅ uma entrada nova
❌ filtros aplicados   → ✅ filtros aplicados ✓
❌ as categorias selecionado → ✅ as categorias selecionadas
❌ nenhum dado encontrado    → ✅ nenhum dado encontrado ✓ / nenhuma transação encontrada
```

### 3. Pontuação e Maiúsculas em Mensagens UI

```
Títulos → Capitalizar primeira palavra apenas:
  ❌ Adicionar Nova Transação   → ✅ Adicionar nova transação
  ❌ filtrar por período        → ✅ Filtrar por período
  ❌ SALDO ATUAL                → ✅ Saldo atual

Botões → Verbo no infinitivo, primeira letra maiúscula:
  ❌ salvar       → ✅ Salvar
  ❌ DELETAR      → ✅ Deletar
  ❌ Criando...   → ✅ Criar (ou "Salvando..." se loading state)

Mensagens de feedback → Completas, com ponto final:
  ❌ Salvo!                        → ✅ Transação salva com sucesso.
  ❌ Erro ao salvar                → ✅ Erro ao salvar a transação. Tente novamente.
  ❌ deletado                      → ✅ Transação excluída com sucesso.
  ❌ Campos obrigatórios faltando  → ✅ Preencha todos os campos obrigatórios.

Labels de campo → Sem dois-pontos no label (o HTML já separa):
  ❌ <label>Valor:</label>    → ✅ <label>Valor</label>
  ❌ <label>Data:</label>     → ✅ <label>Data</label>
```

### 4. Abreviações Consistentes

Usar sempre a versão completa (abreviações geram ambiguidade):

```
❌ desc    → ✅ descricao     (no código) / descrição (no template)
❌ cat     → ✅ categoria
❌ trans   → ✅ transacao     (no código) / transação (no template)
❌ val     → ✅ valor
❌ qtd     → ✅ quantidade
❌ dt      → ✅ data
❌ usr     → ✅ usuario       (no código) / usuário (no template)
❌ msg     → ✅ message       (no código) / mensagem (no template)
```

### 5. Mistura PT/EN no mesmo contexto

```html
<!-- ❌ Misturado -->
<button>Save transação</button>
<p>Seu balance é R$ 100</p>
<label>Transaction Date</label>

<!-- ✅ Consistente em PT (UI) -->
<button>Salvar transação</button>
<p>Seu saldo é R$ 100</p>
<label>Data da transação</label>
```

---

## Erros em Inglês — Checklist

### 1. Nomes de Variáveis/Funções com PT Misturado

```python
# ❌ PT/EN misturado
valorTotal = 100
def get_transacao(id):
def calcular_balance():
class TransacaoForm:
total_entradas = 0

# ✅ Inglês consistente (snake_case para variáveis/funções, PascalCase para classes)
total_value = 100
def get_transaction(id):
def calculate_balance():
class TransactionForm:
total_income = 0
```

### 2. Typos Comuns em Inglês

```python
# ❌ Typos frequentes
recieve       → receive
occured       → occurred
sucessful     → successful
aggregat      → aggregate
caluclate     → calculate
desctiption   → description
authetication → authentication
permision     → permission
formating     → formatting
qurey         → query
```

### 3. Nomenclatura Inconsistente (escolher um padrão)

Escolha um verbo para cada operação e use sempre:

```python
# ❌ Inconsistente
def get_user():
def fetch_transaction():
def load_balance():
def retrieve_category():

# ✅ Padronizado: usar get_ para buscar objetos
def get_user():
def get_transaction():
def get_balance():
def get_category():

# ❌ Inconsistente
def create_transaction():
def add_entry():
def new_record():

# ✅ Padronizado: usar create_ para criar
def create_transaction():
def create_category():
def create_user():
```

### 4. Mensagens de Erro em Inglês (se usadas em logs)

```python
# ❌ Mensagens ruins de log
logger.error("Error!")
logger.error("Something bad happened")
logger.error("Failed")

# ✅ Mensagens descritivas de log (contexto + detalhe)
logger.error("Transaction creation failed: invalid value %s", value)
logger.warning("User %s attempted to access unauthorized transaction %s", user.id, pk)
logger.info("Balance recalculated for user %s: %s", user.id, balance)
```

### 5. Commits e PRs

Formato: `type: short description` (presente, minúsculas, imperativo)

```
# ❌ Ruins
"fixed bug"
"changes"
"atualizando views"
"WIP"
"alterações no form de transação"

# ✅ Corretos
feat: add transaction filter by category
fix: correct balance calculation on delete
refactor: extract filter logic to mixin
style: fix PEP08 violations in views.py
test: add E2E tests for transaction form
docs: update README with setup instructions
```

Tipos válidos: `feat`, `fix`, `refactor`, `style`, `test`, `docs`, `chore`

---

## Glossário do Projeto (PT ↔ EN)

Termos padronizados para uso consistente:

| Conceito | Código (EN) | UI/Template (PT) |
|----------|-------------|-----------------|
| Entrada de dinheiro | `income` / `entrada` | Entrada |
| Saída de dinheiro | `expense` / `saida` | Saída |
| Saldo total | `balance` | Saldo |
| Transação | `transaction` | Transação |
| Categoria | `category` | Categoria |
| Subcategoria | `subcategory` | Subcategoria |
| Período | `period` | Período |
| Data | `date` | Data |
| Valor | `value` / `amount` | Valor |
| Descrição | `description` | Descrição |
| Usuário | `user` | Usuário |
| Perfil | `profile` | Perfil |
| Resumo mensal | `monthly_summary` | Resumo do mês |
| Relatório | `report` | Relatório |
| Filtro | `filter` | Filtro |
| Busca | `search` | Buscar |
| Paginação | `pagination` | — (invisível ao usuário) |
| Criado em | `created_at` | Data de criação |
| Atualizado em | `updated_at` | Última atualização |

---

## Padrões de Mensagens Django

### Mensagens de Sucesso (PT)

```python
from django.contrib import messages

# ✅ Padrão
messages.success(request, "Transação criada com sucesso.")
messages.success(request, "Transação atualizada com sucesso.")
messages.success(request, "Transação excluída com sucesso.")
messages.success(request, "Categoria criada com sucesso.")
messages.success(request, "Senha alterada com sucesso.")
```

### Mensagens de Erro (PT)

```python
# ✅ Padrão
messages.error(request, "Erro ao salvar a transação. Tente novamente.")
messages.error(request, "Acesso negado.")
messages.error(request, "Transação não encontrada.")
messages.warning(request, "Preencha todos os campos obrigatórios.")
messages.warning(request, "Valor deve ser maior que zero.")
```

### Validação de Forms (PT)

```python
# forms.py
class TransactionForm(forms.ModelForm):
    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")
        return value

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date > date.today():
            raise forms.ValidationError("A data não pode ser no futuro.")
        return date
```

---

## Checklist Rápido (antes de commit)

### Código Python

- [ ] Nomes em inglês (`snake_case` para funções/variáveis, `PascalCase` para classes)
- [ ] Sem palavras PT em nomes de código (`valor`, `transacao`, `usuario`)
- [ ] Comentários em inglês
- [ ] Sem typos nos identificadores
- [ ] Mesma convenção de verbo (`get_`, `create_`, `update_`, `delete_`)

### Templates HTML

- [ ] Textos visíveis ao usuário em PT
- [ ] Acentos corretos em todo o texto
- [ ] Títulos: só primeira letra maiúscula
- [ ] Botões: verbo no infinitivo, primeira letra maiúscula
- [ ] Mensagens completas com ponto final
- [ ] Labels sem dois-pontos

### Commits

- [ ] Formato `type: description` em inglês
- [ ] Imperativo, minúsculas, sem ponto final
- [ ] Tipo correto (`feat`, `fix`, `refactor`, etc.)

---

## Exemplos Práticos

### Revisão de Template

```html
<!-- ❌ Vários erros -->
<h1>ADICIONAR TRANSACAO</h1>
<label>Valor:</label>
<label>Data:</label>
<button>salvar</button>
<p>transação salvo com Sucesso!</p>

<!-- ✅ Corrigido -->
<h1>Adicionar transação</h1>
<label>Valor</label>
<label>Data</label>
<button>Salvar</button>
<p>Transação salva com sucesso.</p>
```

### Revisão de views.py

```python
# ❌ Vários erros
def get_transacoes(usr):          # PT no nome + abreviação
    lst = []                       # nome sem significado
    for t in Transaction.objects.filter(usuario=usr):
        lst.append(t)
    return lst

# ✅ Corrigido
def get_transactions(user):
    return list(Transaction.objects.filter(user=user))
```

### Revisão de Commit

```
# ❌
"adicionei o filtro de transacao por data"
"fix bugs"

# ✅
feat: add transaction date range filter
fix: resolve balance calculation on delete
```

---

## Integração com @code-review

Combine com `@code-review` para revisão completa:

1. `@code-review` → verifica estrutura, DRY, segurança
2. `@writing-standards` → verifica idioma, typos, mensagens, commits

Juntos cobrem 100% da qualidade do código.
