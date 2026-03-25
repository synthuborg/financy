# Plano: Script de Seed para Popular a Aplicação

**Data:** 2026-03-25  
**Feature:** `seed` — popular BD com dados realistas para desenvolvimento/demo  
**Tipo:** Management Command Django  

---

## Escopo

Criar um `management command` Django (`python manage.py seed`) que popule o banco com:

- 1 usuário demo (`demo@smartfinancy.com` / `demo1234`)
- Categorias de entrada e saída com keywords
- Contas correntes e cartões de crédito
- Transações realistas nos últimos 6 meses
- Metas de economia

**Fora do escopo:** dados de produção, múltiplos usuários.

---

## Checklist TDD

### Planejamento
- [x] Escopo definido
- [x] Impacto mapeado (nenhum model novo)
- [x] Decisão: Management Command (idiomatic Django, sem DRF)

### Implementação
- [x] Criar `finances/management/__init__.py`  
- [x] Criar `finances/management/commands/__init__.py`
- [x] Criar `finances/management/commands/seed.py`
- [x] Usuário demo com `get_or_create`
- [x] Categorias entrada/saída com keywords
- [x] Contas correntes e cartões de crédito
- [x] Transações realistas (6 meses, aleatórias mas coerentes)
- [x] Metas com progresso variado
- [x] Flag `--flush` para limpar e re-popular
- [x] Idempotente (seguro de rodar múltiplas vezes)

### Qualidade
- [x] Sem credenciais hardcoded em produção (apenas modo DEBUG/dev)
- [x] Output amigável com contagens
- [x] `python manage.py check` sem erros
