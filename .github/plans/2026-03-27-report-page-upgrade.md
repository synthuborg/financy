# Plano: Report Page Upgrade

**Data:** 2026-03-27
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Aprimorar a pagina de relatorios financeiros em Django/Tailwind com conteudo util (resumo do periodo, KPIs e secao auxiliar) e mover o formulario atual para um modal acionado pelo botao "Exportar", com fechamento por ESC e botao cancelar.

---

## Escopo

### Incluido
- Reestruturar a pagina de relatorios para destacar informacoes de valor ao usuario.
- Adicionar bloco de resumo do periodo com contexto do filtro ativo.
- Adicionar KPIs principais (ex.: total receitas, total despesas, saldo, variacao).
- Adicionar secao auxiliar com orientacoes/proximos passos de leitura do relatorio.
- Mover o formulario de exportacao atual para modal acionado por "Exportar".
- Garantir fechamento do modal por tecla ESC.
- Garantir fechamento do modal por botao "Cancelar".
- Manter compatibilidade com layout responsivo em Tailwind.

### Fora de escopo
- Criacao de novos endpoints de exportacao com formatos adicionais.
- Alteracao de regras de negocio dos calculos financeiros existentes.
- Refatoracao ampla de design system fora da pagina de relatorios.
- Internacionalizacao (i18n) completa da tela.

---

## Checklist de Execucao

### Backend
- [ ] Ler django-patterns
- [ ] Escrever testes (RED) para dados exibidos no resumo/KPIs da pagina
- [ ] Implementar (GREEN) ajustes de view/contexto para alimentar blocos da pagina
- [ ] Refatorar e executar code-review
- [ ] Commit com git-workflow

### Frontend
- [ ] Ler frontend-finance-design e htmx-patterns
- [ ] Escrever testes (RED) para comportamento do modal (abertura/fechamento)
- [ ] Implementar (GREEN) novos blocos visuais: resumo do periodo, KPIs e secao auxiliar
- [ ] Implementar (GREEN) migracao do formulario para modal acionado por botao "Exportar"
- [ ] Implementar (GREEN) fechamento do modal por ESC e por botao "Cancelar"
- [ ] Validar responsividade e acessibilidade

### Testes
- [ ] Ler testing-workflow e playwright-automation
- [ ] Testes unitarios/integracao passando
- [ ] Testes E2E Playwright passando

### Validacao Manual
- [ ] Abrir a pagina de relatorios e confirmar renderizacao dos blocos de resumo, KPIs e secao auxiliar
- [ ] Confirmar que o formulario nao aparece inline e apenas no modal
- [ ] Clicar em "Exportar" e validar abertura do modal
- [ ] Pressionar ESC e validar fechamento do modal
- [ ] Abrir novamente o modal e fechar por "Cancelar"
- [ ] Confirmar que o foco retorna para o botao "Exportar" apos fechar o modal
- [ ] Validar comportamento em mobile (>=375px) e desktop

### Dependencies
- [ ] requirements/requirements.txt atualizado (se aplicavel)

### Documentacao
- [ ] README Curator invocado

---

## Riscos e Premissas
- Risco: quebra de fluxo atual de exportacao ao mover formulario para modal.
- Risco: conflito de comportamento entre HTMX e scripts existentes na pagina.
- Risco: regressao de acessibilidade (foco, navegacao por teclado, fechamento por ESC).
- Risco: inconsistencias de layout em breakpoints menores.
- Premissa: o endpoint/acao de exportacao atual continuara o mesmo.
- Premissa: o botao "Exportar" ja existe e pode ser reutilizado como gatilho do modal.
- Premissa: os dados necessarios para KPIs ja podem ser derivados do contexto atual da pagina.

---

## Log de Progresso
- 2026-03-27: Plano criado em .github/plans/2026-03-27-report-page-upgrade.md com escopo, checklist por trilha, validacao manual e riscos.

---

## Validacao Final
- [ ] Todos os itens do checklist marcados
- [ ] Testes passando
- [ ] README atualizado
- [ ] Sem itens bloqueados
