# Plano: Telegram Bot para Lancamentos no Financy

**Data:** 2026-03-27
**Status:** Em andamento
**Agente:** Planner Checklist

---

## Objetivo
> Implementar lancamentos financeiros via Telegram por usuario, com isolamento multitenant e armazenamento seguro de credenciais (hash de token/chat_id e token cifrado operacional), refletindo os dados no dashboard do Financy.

---

## Escopo

### Incluido
- App separado `telegram_bot` no projeto Financy.
- Onboarding por usuario autenticado para conectar/desconectar bot.
- Webhook Telegram com roteamento seguro por usuario (sem fallback cross-user).
- Parse de linguagem natural para criar Transaction (entrada/saida).
- Classificacao automatica de categoria via Category.keywords do proprio usuario.
- Atualizacao de dashboard com HTMX apos novos lancamentos.
- Comandos de bot: /listar, /saldo, /excluir, /ajuda.
- Persistencia segura: hash deterministico de chat_id, hash de token, token cifrado operacional.
- Testes unitarios/integracao/E2E para fluxos criticos, seguranca e isolamento.

### Fora de escopo
- Suporte a multiplos bots por usuario na primeira entrega.
- NLP avancado com LLM externo.
- Sincronizacao retroativa de historico de mensagens do Telegram.
- Analytics avancado de uso do bot.

---

## Criterios de Aceite
- Fluxo completo funcional: conectar bot -> enviar mensagem -> criar Transaction -> dashboard atualizado.
- Webhook responde HTTP 200 em todos os casos validos/invalidos tratados para evitar retries indevidos.
- Lookup de usuario no webhook usa chat_id hash e escopo seguro por usuario.
- Token e chat_id nunca sao salvos em texto puro no banco.
- Token operacional e armazenado cifrado e usado apenas quando necessario para chamada da API Telegram.
- Multitenancy validado: um usuario nao acessa/configura/processa dados de outro usuario.
- Testes cobrindo parse NLP, criacao de Transaction, isolamento, seguranca de armazenamento e endpoints principais.

---

## Ordem de Execucao
1. Levantamento tecnico e desenho de dados/seguranca.
2. TDD de modelos/servicos de credenciais (RED -> GREEN -> refactor).
3. TDD de onboarding (validar token/chat_id, conectar/desconectar).
4. TDD de webhook e parse NLP para lancamentos/comandos.
5. Integracao HTMX/dashboard e feedback visual.
6. Testes E2E Playwright do fluxo ponta a ponta.
7. Revisao final, documentacao e commit.

---

## Checklist de Execucao

### Backend
- [x] Skill lida: django-patterns.
- [x] Skill lida: code-review.
- [ ] Definir modelo `telegram_bot` com campos: user (OneToOne), token_hash, token_encrypted, chat_id_hash, ativo, timestamps.
- [ ] Definir indices/constraints para lookup rapido e unicidade segura por usuario/chat.
- [ ] Escrever testes RED de model/service para hash e cifragem (sem texto puro).
- [ ] Implementar GREEN de hashing deterministico (chat_id) e hashing de token para auditoria.
- [ ] Implementar GREEN de cifragem de token operacional com chave via env.
- [ ] Refatorar services e aplicar checklist code-review.
- [ ] Escrever testes RED de onboarding (validar token, detectar chat_id, conectar, desconectar).
- [ ] Implementar GREEN de endpoints de onboarding com auth e ownership.
- [ ] Escrever testes RED do webhook multitenant e comandos (/listar, /saldo, /excluir, /ajuda).
- [ ] Implementar GREEN do webhook com resposta 200 e sem fallback cross-user.
- [ ] Implementar parser NLP (receita/despesa -> entrada/saida) com validacoes de valor/data/descricao.
- [ ] Implementar criacao de Transaction e categorizacao por Category.keywords do usuario.
- [ ] Refatorar views para orquestracao e services para regra de negocio.
- [ ] Commit com git-workflow.

### Frontend
- [ ] Ler frontend-finance-design e htmx-patterns.
- [ ] Criar UI de onboarding Telegram no padrao visual do projeto.
- [ ] Implementar estados de conexao/desconexao e feedback de erros de validacao.
- [ ] Implementar fragmento HTMX para atualizar lista/dashboard apos novos lancamentos.
- [ ] Validar responsividade e acessibilidade basica das telas.

### Testes
- [x] Skill lida: testing-workflow.
- [x] Skill lida: playwright-automation.
- [ ] Unit tests: hash/cifra, parser NLP, comandos, regras de negocio.
- [ ] Integration tests: onboarding + webhook + Transaction.
- [ ] Testes de seguranca: garantir ausencia de token/chat_id em texto puro no banco e logs.
- [ ] Testes de isolamento: usuarios A/B com tokens/chat_id distintos sem vazamento.
- [ ] E2E Playwright: conectar bot, enviar evento webhook simulado, validar dashboard.
- [ ] Suite completa passando (pytest + playwright).

### Dependencies
- [ ] Atualizar requirements/requirements.txt (se houver nova dependencia criptografica).
- [ ] Registrar variaveis de ambiente necessarias no setup.

### Documentacao
- [ ] Atualizar README com configuracao do telegram_bot, env vars e fluxo de onboarding.
- [ ] Documentar payload de webhook e comandos suportados.

---

## Riscos e Premissas
- Risco: chave de cifragem mal configurada em ambiente pode bloquear onboarding.
- Risco: parse NLP ambiguidade em mensagens curtas pode gerar classificacao incorreta.
- Risco: retries do Telegram podem duplicar lancamentos sem estrategia idempotente.
- Premissa: ha endpoint publico HTTPS disponivel para webhook do Telegram.
- Premissa: modelo Transaction atual suporta criacao via service sem alterar contrato principal.
- Premissa: usuarios ja autenticam no Financy antes de conectar bot.

---

## Log de Progresso
- 2026-03-27: Prompt da feature e skills relevantes lidos; plano detalhado criado com TDD, seguranca e ordem de execucao.

---

## Validacao Final
- [ ] Todos os itens do checklist marcados
- [ ] Testes passando
- [ ] README atualizado
- [ ] Sem itens bloqueados
