---
description: "Adicionar tema light em app já dark, com alternância de tema global e persistência"
name: "Implementar Light + Dark Theme"
argument-hint: "Informe páginas/áreas prioritárias, stack de estilos e restrições visuais"
agent: "agent"
---

Implemente suporte completo a tema Light e Dark em toda a aplicação, considerando que o Dark já existe e é o tema atual.

Contexto adicional do usuário:
$ARGUMENTS

Objetivo principal:
1. Manter o tema Dark existente funcionando.
2. Criar o tema Light equivalente em todas as telas e componentes.
3. Adicionar botão global de alternância de tema no header global.
4. Persistir escolha do usuário entre sessões.
5. Executar rollout completo em toda a aplicação de uma vez (sem fatiar por módulo).
6. Respeitar preferência de tema do sistema do usuário quando não houver escolha salva.

Instruções de execução:
1. Mapear rapidamente as fontes de estilo da aplicação (templates, CSS, Tailwind classes, componentes reutilizáveis).
2. Definir tokens de tema (cores de fundo, texto, borda, destaque, estados de sucesso/erro) para Dark e Light.
3. Refatorar estilos hardcoded para usar tokens/classes por tema.
4. Implementar alternância global (toggle) com estado persistido em localStorage.
5. Aplicar tema inicial sem flicker (FOUC), priorizando preferência salva; sem preferência salva, usar `prefers-color-scheme` do sistema.
6. Garantir legibilidade e contraste mínimo adequado em ambos os temas.
7. Atualizar páginas principais e componentes críticos (cards, tabelas, formulários, modais, botões, alertas).
8. Validar comportamento responsivo e consistência visual.
9. Implementar o toggle no header global e propagar seu estado para todo o app.

Critérios de aceite:
1. Toggle visível e funcional no header global.
2. Tema selecionado permanece após reload e novo login.
3. Nenhuma tela principal permanece com estilo quebrado ou ilegível no tema Light.
4. Tema Dark atual não sofre regressão visual.
5. Contraste e estados interativos (hover/focus/disabled) funcionam nos dois temas.
6. Rollout aplicado em toda a aplicação na mesma entrega.
7. Na primeira carga (sem preferência salva), tema segue o sistema do usuário.

Saída esperada (obrigatória):
1. Resumo curto da abordagem adotada.
2. Lista objetiva dos arquivos alterados.
3. Principais decisões de design/tokens.
4. Passos de verificação manual (desktop + mobile).
5. Comandos de validação executados e resultado.

Se detectar conflito com design existente, priorize preservar padrões já usados no projeto e proponha ajuste incremental em vez de reescrever toda a UI de uma vez.