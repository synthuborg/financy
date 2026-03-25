---
description: "Use when implementing or refactoring Django/Python code. Enforce architecture, naming, CBV/DRF design, validation, security, performance, and testing standards."
name: "Django Project Standards"
applyTo: "**/*.py"
---

# Django Project Standards

## Arquitetura e organizacao
- Mantenha responsabilidades separadas: dominio, aplicacao e transporte HTTP.
- Views e ViewSets devem orquestrar requisicao/resposta; regra de negocio vai para service, model method ou dominio.
- Evite funcoes gigantes. Prefira composicao, metodos pequenos e nomes autoexplicativos.

## CBV e DRF
- Para CRUD comum, prefira Generic CBV/GenericAPIView/ViewSet.
- Em CBV, sobrescreva apenas metodos necessarios e mantenha fluxo explicito.
- Em DRF, serializers validam e transformam dados; nao centralize regra de negocio complexa no serializer.

## Validacao e dados
- Validacoes de dominio devem existir no backend (model/form/serializer/service).
- Nunca dependa apenas de validacao de frontend.
- Use transacoes quando operacoes dependem de consistencia atomica.

## Seguranca
- Exija autenticacao/autorizacao no servidor para toda acao sensivel.
- Aplique permissao por objeto quando necessario.
- Previna exposicao de campos sensiveis em serializers e respostas.
- Evite buscar objetos sem escopo do usuario quando o recurso for privado.

## Performance
- Revise consultas em listagens: use select_related/prefetch_related quando fizer sentido.
- Evite N+1 em views, services e serializers.
- Paginacao deve ser obrigatoria em colecoes de API.

## Qualidade e testes
- Toda mudanca de comportamento deve ter teste correspondente.
- Cubra sucesso, falha de validacao, autenticacao/autorizacao e regressao.
- Para APIs, sempre validar status code e contrato basico de resposta.

## Manutenibilidade
- Nomes devem refletir intencao de negocio.
- Evite comentarios obvios; documente apenas decisao importante e tradeoff.
- Preserve compatibilidade de rotas/contratos ou documente migracao.
