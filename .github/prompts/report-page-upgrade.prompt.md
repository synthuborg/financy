---
description: "Use quando precisar evoluir a pagina de relatorios financeiros no Django/Tailwind com mais conteudo util e modal acionado por botao Exportar"
name: "Report Page Upgrade"
argument-hint: "informe rota/template alvo, objetivo do relatorio e formato(s) de exportacao"
agent: "Frontend Specialist"
---

Atue como Frontend Specialist em Django Templates (Tailwind), preservando a logica de negocio existente.

Tarefa unica:
Aprimorar a pagina de relatorios para deixar de ser um bloco simples de formulario e virar uma tela completa de relatorios, com contexto visual e fluxo de exportacao orientado por acao.

Objetivo funcional obrigatorio:
- O componente/formulario de importacao/exportacao deve abrir em um modal ao clicar no botao "Exportar".
- O conteudo da pagina deve continuar acessivel e util mesmo sem abrir o modal.

Use os argumentos fornecidos no comando para entender:
- qual template/rota sera alterado;
- quais formatos de exportacao devem existir (PDF, CSV, XLSX, etc.);
- quais KPIs ou secoes devem aparecer na pagina.

Requisitos de implementacao:
1. Estrutura da pagina
- Manter cabecalho com titulo e subtitulo.
- Criar secoes adicionais antes do modal, por exemplo:
  - resumo do periodo (data inicial/final e total de lancamentos);
  - cards de KPIs (entradas, saidas, saldo, ticket medio);
  - lista de relatorios recentes ou atalhos de exportacao.

2. Acao de Exportar
- Inserir botao principal "Exportar" na area de acoes da pagina.
- Ao clicar, abrir modal com o formulario de exportacao/importacao existente.
- Modal com:
  - overlay escuro;
  - fechamento por botao "Cancelar" e tecla ESC;
  - bloqueio de clique acidental fora do card (ou comportamento explicitado no codigo).

3. Qualidade de UX
- Estados visuais de hover/focus claros.
- Layout responsivo (mobile e desktop).
- Sem regressao no fluxo atual de envio do formulario.

4. Limites tecnicos
- Nao quebrar URLs, nomes de campos, csrf, metodos HTTP ou contratos existentes.
- Evitar JS complexo quando HTMX/Alpine resolver de forma simples.
- Se criar script inline, manter pequeno e legivel.

Entrega esperada:
1. Codigo final pronto para uso (template(s) e ajustes minimos relacionados).
2. Resumo curto do que foi melhorado na pagina.
3. Checklist de validacao manual:
- botao Exportar abre modal;
- modal fecha corretamente;
- submit continua funcionando;
- layout ok em mobile e desktop.

Se houver ambiguidade de requisitos, assuma a opcao mais segura para preservar comportamento atual e documente a decisao no resumo final.
