# Plano: Orcamento Mensal com Alertas Telegram

**Data:** 2026-03-28
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Implementar controle de orcamento mensal com limite por percentual da renda mensal manual, limite diario dinamico e alertas Telegram configuraveis para prevencao e acompanhamento de gastos.

---

## Escopo

### Incluido
- Cadastro e atualizacao de orcamento mensal por usuario com percentual manual da renda mensal.
- Calculo do limite mensal absoluto a partir de renda mensal manual x percentual configurado.
- Calculo de limite diario dinamico com base no saldo de orcamento restante e dias restantes do mes.
- Regras de alerta Telegram nos marcos de consumo: 20% restante, 10% restante e 100% do limite mensal consumido.
- Regra adicional: apos ultrapassar 100%, enviar alerta Telegram a cada nova despesa registrada.
- Opcao por usuario para desabilitar alertas de orcamento no Telegram.
- Card fixo de alertas de orcamento no dashboard com estado atual (restante, percentual consumido, limite diario).
- Calendario no dashboard com percentual consumido por dia e quantidade de despesas por dia.
- Cobertura de testes unitarios e testes de integracao para regras de negocio, notificacoes e exibicao de dados no dashboard.

### Fora de escopo
- Integracoes com canais diferentes de Telegram.
- Sugestao automatica de categoria de gastos por IA.
- Edicao em lote de despesas antigas para recalculo retroativo complexo fora do mes corrente.

---

## Checklist de Execucao

### Backend
- [ ] Ler skill django-patterns e aplicar padroes CBV/services/selectors.
- [ ] Ler skill code-review e alinhar criterios de qualidade e seguranca.
- [ ] Escrever testes (RED) para modelo/servico de configuracao de orcamento mensal por percentual da renda manual.
- [ ] Implementar (GREEN) persistencia e validacoes de orcamento mensal.
- [ ] Escrever testes (RED) para calculo de limite diario dinamico.
- [ ] Implementar (GREEN) servico de calculo diario dinamico com regras de dias restantes.
- [ ] Escrever testes (RED) para regras de disparo de alertas (20%/10%/100% e pos-limite por despesa).
- [ ] Implementar (GREEN) orquestracao de alertas Telegram com controle de marcos ja notificados.
- [ ] Escrever testes (RED) para opcao de desabilitar alertas por usuario.
- [ ] Implementar (GREEN) flag/configuracao para desabilitar alertas de orcamento.
- [ ] Refatorar e executar checklist da skill code-review.
- [ ] Commit com skill git-workflow.

### Frontend
- [ ] Ler skills frontend-finance-design e htmx-patterns para guia visual/interativo.
- [ ] Escrever testes (RED) de integracao para renderizacao do card fixo de alertas no dashboard.
- [ ] Implementar (GREEN) card fixo com resumo de limite mensal, consumo, restante e limite diario.
- [ ] Escrever testes (RED) de integracao para calendario com percentual e quantidade de despesas por dia.
- [ ] Implementar (GREEN) calendario de gastos diarios no dashboard.
- [ ] Implementar opcao visual de habilitar/desabilitar alertas Telegram de orcamento.
- [ ] Validar responsividade e acessibilidade (desktop/mobile).

### Testes
- [ ] Ler skill testing-workflow para estrategia final de cobertura.
- [ ] Escrever/ajustar testes unitarios para services/selectors/forms relacionados ao orcamento.
- [ ] Escrever/ajustar testes de integracao para fluxo dashboard + Telegram + configuracao de alertas.
- [ ] Executar suite de testes e corrigir regressos.
- [ ] Ler skill playwright-automation e avaliar cobertura E2E minima para fluxo critico.
- [ ] Testes E2E Playwright passando (se fluxo ja estiver automatizado no projeto).

### Dependencies
- [ ] requirements/requirements.txt atualizado (se aplicavel).

### Documentacao
- [ ] README Curator invocado.
- [ ] Atualizar README com configuracao de orcamento mensal e regras de alerta Telegram.

---

## Riscos e Premissas
- Risco: duplicidade de alertas quando houver multiplas despesas em curto intervalo sem controle idempotente.
- Risco: calculo diario divergente em virada de mes/fuso horario se base temporal nao for padronizada.
- Risco: sobrecarga de mensagens Telegram apos limite se usuario registrar muitas despesas em sequencia.
- Premissa: renda mensal manual ja existe ou sera adicionada de forma simples no mesmo fluxo de configuracao.
- Premissa: bot Telegram e identificacao do usuario Telegram ja estao funcionais no ambiente.

---

## Log de Progresso
- 2026-03-28: plano inicial criado com escopo, checklist por track e estrategia TDD (RED -> GREEN).

---

## Validacao Final
- [ ] Todos os itens do checklist marcados.
- [ ] Testes passando.
- [ ] README atualizado.
- [ ] Sem itens bloqueados.
