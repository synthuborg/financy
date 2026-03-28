---
description: "Use quando precisar implementar orcamento mensal com limite de gastos por percentual da renda, calendario diario e alertas no Telegram + dashboard"
name: "Orcamento Mensal com Alertas Telegram"
argument-hint: "informe regra de limite, comportamento dos alertas e detalhes da interface"
agent: "app-builder"
---

Atue como app-builder para implementar uma feature completa de orcamento mensal no FinTrack, com foco em controle preventivo de gastos e alertas automáticos.

Contexto adicional do usuario:
$ARGUMENTS

Objetivo principal:
1. Permitir definir um teto mensal de gastos baseado em percentual da renda (exemplo: 80% da renda mensal).
2. Exibir um calendario de acompanhamento diario com:
- valor maximo recomendado para gastar por dia para manter a meta mensal;
- numero de despesas lancadas no dia;
- indicador percentual de consumo da meta.
3. Exibir barra de progresso de despesas em percentual em relacao ao limite mensal.
4. Integrar alertas com o bot Telegram ja existente no projeto.
5. Exibir os mesmos alertas no dashboard da aplicacao.
6. Permitir o usuario habilitar ou desabilitar alertas.

Decisoes de produto ja confirmadas:
1. A renda-base do orcamento mensal e um valor fixo manual definido pelo usuario para o mes.
2. O limite diario recomendado deve ser recalculado dinamicamente todos os dias com base no saldo restante do orcamento e dias restantes do mes.
3. No dashboard, os alertas devem aparecer em um card fixo no topo.
4. Apos ultrapassar o limite, o Telegram deve enviar alerta a cada nova despesa, sem intervalo minimo.

Regras funcionais obrigatorias de alerta:
1. Quando faltar 20% para atingir o limite mensal, enviar alerta Telegram e exibir alerta no dashboard.
2. Quando faltar 10% para atingir o limite mensal, enviar novo alerta Telegram e exibir alerta no dashboard.
3. Quando atingir 100% do limite, enviar alerta Telegram e exibir alerta no dashboard.
4. Apos ultrapassar o limite, enviar alerta a cada nova despesa lancada.

Requisitos tecnicos e de arquitetura:
1. Seguir o padrao do projeto: views apenas orquestram; regras em services; leitura em selectors.
2. Garantir isolamento por usuario em todas as consultas e operacoes.
3. Reusar a infraestrutura atual do app telegram_bot para envio de mensagens.
4. Tratar idempotencia dos alertas de 20%, 10% e 100% para evitar envios duplicados no mesmo ciclo mensal.
5. Permitir reset natural no inicio de cada novo mes.
6. Criar migracoes necessarias para novos modelos/campos.
7. Incluir configuracao de preferencias de alerta no fluxo do usuario.

Requisitos de UX/UI:
1. Adicionar tela/configuracao de orcamento mensal com percentual alvo editavel.
2. Exibir componente visual de progresso mensal (barra percentual).
3. Exibir calendario mensal com estado por dia (gasto, quantidade de despesas, limite diario recomendado).
4. Exibir alertas no dashboard em destaque, com estado claro (atencao, limite atingido, limite excedido).
5. Garantir boa experiencia em desktop e mobile.

Requisitos de testes:
1. Testes unitarios para regras de calculo de limite mensal e limite diario.
2. Testes unitarios para gatilhos de alerta (20%, 10%, 100%, acima de 100% por nova despesa).
3. Testes de integracao para fluxo de cadastro/edicao de orcamento e exibicao no dashboard.
4. Testes garantindo que usuario com alertas desabilitados nao recebe notificacoes.
5. Testes garantindo escopo por usuario e ausencia de regressao.

Entrega esperada:
1. Implementacao completa (models, migrations, services, selectors, views, urls, templates).
2. Testes automatizados cobrindo regras de negocio e fluxo principal.
3. Resumo final com:
- arquivos alterados;
- decisoes tecnicas relevantes;
- comandos executados e resultados;
- passos de validacao manual.

Se houver ambiguidade de produto, adote defaults seguros e documente claramente no resumo final as suposicoes adotadas.
