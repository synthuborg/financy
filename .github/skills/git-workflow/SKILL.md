---
name: git-workflow
description: Git workflow for hackaton_app_financas. Generate clear Conventional Commits based on what was changed, stage correctly, push safely, and write good PR descriptions.
instructions: |
  When asked to commit or push code, follow the full workflow: pull → stage → commit → push.
  Generate commit messages using Conventional Commits format based on what actually changed.
  Keep messages short, clear, and in English.
keywords: [git, commit, push, branch, github, conventional-commits, pr, workflow]
---

# Git Workflow — hackaton_app_financas

Fluxo completo: do código no editor até o GitHub, com commits claros e simples.

---

## Fluxo Padrão (do início ao fim)

```
1. git pull          ← sincronizar antes de começar
2. [fazer mudanças]  ← código, templates, testes
3. git add           ← selecionar o que vai no commit
4. git commit -m     ← mensagem clara baseada no que mudou
5. git push          ← subir para GitHub
```

---

## 1. Sincronizar Antes de Trabalhar

```bash
git pull origin main
```

Se houver conflito:
```bash
git status          # ver arquivos em conflito
# Resolver conflitos manualmente
git add .
git commit -m "merge: resolve conflicts on main"
```

---

## 2. Staging — O que incluir no commit

### Ver o que mudou

```bash
git status          # arquivos modificados
git diff            # ver mudanças linha a linha
git diff --staged   # ver o que já está no stage
```

### Adicionar arquivos

```bash
# Tudo de uma vez (use quando todas as mudanças pertencem ao mesmo commit)
git add .

# Arquivo específico (use quando quer separar em commits distintos)
git add apps/transactions/views.py
git add templates/transactions/list.html

# Por pasta
git add apps/transactions/
git add templates/

# Interativo (escolhe linha por linha)
git add -p
```

### Quando separar em commits distintos

```bash
# ✅ 1 commit por funcionalidade/correção
git add apps/transactions/views.py templates/transactions/
git commit -m "feat: add transaction category filter"

git add apps/categories/
git commit -m "feat: add category CRUD"
```

---

## 3. Gerar Mensagem de Commit

### Formato Conventional Commits

```
type: short description

[optional body - if needed]
```

- **type**: o que foi feito
- **description**: o que especificamente (imperativo, inglês, minúsculas, sem ponto)
- **body** (opcional): por quê ou como, só se não for óbvio

### Tipos e Quando Usar

| Type | Quando usar | Exemplo |
|------|------------|---------|
| `feat` | Nova funcionalidade | `feat: add transaction filter by category` |
| `fix` | Corrigir bug | `fix: correct balance calculation on delete` |
| `style` | UI, CSS, HTML visual (sem lógica) | `style: adjust sidebar spacing on mobile` |
| `refactor` | Reorganizar código sem mudar comportamento | `refactor: extract filter logic to mixin` |
| `test` | Adicionar ou corrigir testes | `test: add E2E tests for transaction form` |
| `docs` | README, comentários, documentação | `docs: add setup instructions to README` |
| `chore` | Config, dependências, CI | `chore: add playwright to package.json` |
| `perf` | Melhoria de performance | `perf: add select_related to transaction query` |

---

## 4. Como Gerar a Mensagem Baseada no Que Mudou

Ao pedir para gerar um commit, descreva o que foi feito e a skill monta a mensagem:

### Exemplos por tipo de mudança

**Criou nova feature:**
```
Você: "adicionei a tela de filtrar transações por categoria"
→ feat: add transaction category filter
```

**Corrigiu bug:**
```
Você: "o saldo estava calculando errado quando deletava transação"
→ fix: correct balance recalculation on transaction delete
```

**Mudou estilo/layout:**
```
Você: "ajustei o espaçamento do sidebar no mobile"
→ style: fix sidebar spacing on mobile screens
```

**Refatorou código:**
```
Você: "tirei código duplicado das views de entrada e saída"
→ refactor: extract shared logic to BaseTransactionView
```

**Adicionou testes:**
```
Você: "escrevi testes E2E para o formulário de transação"
→ test: add E2E tests for transaction create form
```

**Múltiplas mudanças pequenas:**
```
Você: "corrigi acentos nos templates, melhorei o espaçamento e removi imports não usados"
→ Separar em 3 commits:
   style: fix Portuguese accents in transaction templates
   style: improve spacing on dashboard cards
   chore: remove unused imports from views.py
```

---

## 5. Push para o GitHub

```bash
# Push para main (fluxo hackaton)
git push origin main

# Se der erro "rejected" (alguém pushou antes)
git pull origin main --rebase
git push origin main
```

### Verificar antes de pushear

```bash
git log --oneline -5    # ver últimos commits
git diff origin/main    # ver o que vai subir
```

---

## 6. Pull Request (PR)

### Título do PR

Mesmo formato do commit, mas pode ser mais descritivo:

```
# ✅ Bons títulos
feat: add transaction filter and search
fix: resolve balance calculation after delete
feat: add category management (CRUD)

# ❌ Ruins
"updates"
"changes"
"wip"
"atualizações diversas"
```

### Descrição do PR

Template simples:

```markdown
## O que foi feito
- Adicionado filtro de transações por categoria
- Live search com HTMX (debounce 300ms)
- Paginação com 20 itens por página

## Como testar
1. Ir para `/transactions/`
2. Clicar em uma categoria
3. Ver lista filtrar sem recarregar página

## Checklist
- [x] Código em inglês
- [x] Templates em português
- [x] Sem console.log esquecidos
- [x] PEP08 ok
```

---

## Referência Rápida — Comandos do Dia a Dia

```bash
# Ver estado atual
git status
git log --oneline -10

# Desfazer mudanças não commitadas
git restore arquivo.py         # desfaz mudança em 1 arquivo
git restore .                  # desfaz tudo (cuidado!)
git restore --staged arquivo   # tira do stage sem desfazer

# Corrigir último commit (antes de pushear)
git commit --amend -m "feat: new message"

# Ver histórico resumido
git log --oneline --graph
```

---

## Checklist Antes de Pushear

- [ ] `git pull` feito antes de começar
- [ ] Só arquivos relevantes no `git add` (sem `.env`, `__pycache__`, `.pyc`)
- [ ] Mensagem no formato `type: description`
- [ ] Descrição em inglês, imperativo, minúsculas
- [ ] 1 commit = 1 mudança coesa (não misturar feat + fix)
- [ ] Sem arquivos sensíveis (`.env`, senhas, tokens)

---

## .gitignore — Nunca Subir

Certifique-se que o `.gitignore` do projeto contém:

```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/

# Django
*.log
local_settings.py
db.sqlite3
media/

# Environment
.env
.env.*
venv/
env/
.venv/

# Node
node_modules/
npm-debug.log

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# Playwright
test-results/
playwright-report/
```

---

## Integração com @writing-standards

Antes de commitar, a mensagem deve seguir @writing-standards:

```bash
# ✅ Commit com padrão correto
git commit -m "feat: add transaction filter by date range"
#                    ^EN  ^imperativo  ^snake-case implícito

# ❌ Erros comuns
git commit -m "Adicionei filtro"        # PT + passado
git commit -m "feat: adds filter"       # 's' errado
git commit -m "feat: Add Filter"        # maiúsculas
git commit -m "feat: add filter."       # ponto no final
```
