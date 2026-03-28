---
description: "Use quando precisar mover a configuracao de orcamento do layout fixo para um modal, com botao de abertura e controles de alertas"
name: "Orcamento: Configuracao em Modal"
argument-hint: "informe pagina alvo, comportamento do modal e regras de configuracao de alertas"
agent: "Frontend Specialist"
---

Atue como Frontend Specialist para refatorar a interface de orcamento no FinTrack.

Contexto adicional do usuario:
$ARGUMENTS

Objetivo principal:
1. Remover o card fixo de configuracao que aparece ao lado do calendario.
2. Substituir esse card por um modal de configuracao.
3. Adicionar um botao claro de "Configurar" para abrir o modal.
4. Incluir no modal a secao de configuracao de alertas (habilitar/desabilitar e campos relacionados, quando existirem).
5. No componente da area de orcamento/calendario, mudar o container principal de layout horizontal (flex row) para layout vertical (flex column).

Regras de UX obrigatorias:
1. O calendario de gastos deve continuar visivel na pagina principal sem competir com o formulario.
2. O botao de configuracao deve ficar em posicao de facil acesso (cabecalho do bloco de orcamento ou area de acoes).
3. O modal deve ter: titulo, descricao curta, formulario, botao de salvar e botao de cancelar/fechar.
4. O modal deve permitir fechar por:
- botao de fechar;
- tecla ESC;
- clique no backdrop (se nao houver risco de perda de dados nao salvos).
5. Preservar responsividade (mobile e desktop) e contraste visual no tema atual.

Regras tecnicas:
1. Preservar o fluxo atual de submit do formulario (POST existente), sem quebrar validacoes server-side.
2. Reaproveitar classes e componentes existentes do projeto antes de criar novos estilos.
3. Evitar dependencia de JavaScript complexo; preferir HTMX/Alpine ja adotados no projeto.
4. Garantir que erros de validacao do formulario aparecam no modal com feedback claro.
5. Se o submit falhar por validacao, reabrir o modal automaticamente mantendo valores preenchidos.
6. Ajustar classes utilitarias do componente para refletir a mudanca de flex row para flex column sem quebrar mobile/desktop.

Escopo minimo de alteracoes esperadas:
1. Template da pagina de orcamento e/ou fragmento relacionado ao card atual.
2. Ajustes de markup para trigger do modal e container do formulario.
3. Ajustes pontuais de view/contexto apenas se necessarios para controlar estado do modal.
4. Testes de regressao para:
- presenca do botao de configuracao;
- ausencia do card fixo antigo;
- renderizacao da secao de alertas dentro do modal;
- submit funcionando.

Criterios de aceite:
1. A pagina nao exibe mais o card de configuracao fixo ao lado do calendario.
2. Existe botao de configuracao funcional que abre modal.
3. O modal contem configuracoes de orcamento e secao de alertas.
4. Salvar continua funcionando com feedback de sucesso/erro.
5. O componente do calendario usa layout em coluna (nao em linha) na estrutura principal.
6. Layout permanece consistente no mobile e no desktop.

Entrega esperada:
1. Lista objetiva dos arquivos alterados.
2. Resumo das decisoes de UX e acessibilidade aplicadas.
3. Comandos executados e resultado dos testes.
4. Observacoes de compatibilidade (ex.: fallback sem JS, se aplicavel).

Se houver ambiguidade de produto, use defaults seguros e documente as suposicoes no resumo final.
