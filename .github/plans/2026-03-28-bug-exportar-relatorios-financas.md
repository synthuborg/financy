# Plano: Correcao do Bug de Exportacao em Relatorios

**Data:** 2026-03-28
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Diagnosticar e corrigir o bug em /financas/relatorios/ no qual o botao "Exportar relatorio" nao dispara acao, garantindo funcionamento correto no backend e template com cobertura de testes e validacao manual.

---

## Escopo

### Incluido
- Reproduzir e diagnosticar o bug de exportacao na rota de relatorios.
- Validar se o gatilho no template (botao/form/modal/HTMX) esta configurado corretamente.
- Validar se a view/URL/acao de exportacao estao ligadas corretamente no backend.
- Escrever testes de regressao para o clique no exportar e resposta esperada.
- Corrigir backend e/ou template conforme causa raiz.
- Validar manualmente o fluxo completo de exportacao.
- Atualizar documentacao se houver mudanca de comportamento ou fluxo.

### Fora de escopo
- Criacao de novos formatos de exportacao.
- Redesign completo da pagina de relatorios.
- Refatoracao ampla de modulos nao relacionados ao bug.

---

## Checklist de Execucao

### Backend
- [ ] Ler django-patterns
- [ ] Escrever testes (RED) cobrindo endpoint/view de exportacao e contratos de resposta
- [ ] Implementar (GREEN) ajuste em view/service/url para restaurar execucao da exportacao
- [ ] Refatorar e executar code-review
- [ ] Commit com git-workflow

### Frontend
- [ ] Ler frontend-finance-design e htmx-patterns
- [ ] Escrever testes (RED) para gatilho do botao Exportar no template (form action, method, hx-* ou submit)
- [ ] Implementar (GREEN) ajuste no template/componente responsavel pelo clique sem acao
- [ ] Validar responsividade e acessibilidade

### Testes
- [ ] Ler testing-workflow e playwright-automation
- [ ] Testes unitarios/integracao passando
- [ ] Testes E2E Playwright passando

### Validacao Manual
- [ ] Acessar /financas/relatorios/ com usuario autenticado
- [ ] Clicar no botao "Exportar relatorio" e confirmar que uma acao e disparada
- [ ] Confirmar request no navegador (metodo/URL/status esperados)
- [ ] Confirmar retorno funcional (download de arquivo, redirecionamento ou feedback visual esperado)
- [ ] Repetir validacao em mobile e desktop

### Dependencies
- [ ] requirements/requirements.txt atualizado (se aplicavel)

### Documentacao
- [ ] README Curator invocado
- [ ] Atualizar README/changelog se fluxo de exportacao ou pre-condicoes mudarem

---

## Riscos e Premissas
- Risco: o problema pode envolver mais de um ponto (template + rota + permissao), aumentando o tempo de diagnostico.
- Risco: possivel regressao em outros botoes/acoes da pagina de relatorios.
- Premissa: existe endpoint de exportacao definido ou esperado para o botao atual.
- Premissa: o comportamento esperado da exportacao (download/retorno) esta definido no produto atual.

---

## Log de Progresso
- 2026-03-28: Plano criado em .github/plans/2026-03-28-bug-exportar-relatorios-financas.md com checklist TDD enxuto para diagnostico, correcao, testes e documentacao.

---

## Validacao Final
- [ ] Todos os itens do checklist marcados
- [ ] Testes passando
- [ ] README atualizado
- [ ] Sem itens bloqueados
