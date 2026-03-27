---
description: "Refatora componentes React + Tailwind para o design system Dark Luxury / Technical"
name: "Dark Luxury Technical Theme"
agent: "agent"
---

Atue como um Engenheiro de Frontend Senior e Especialista em UI/UX.

Tarefa: refatore o codigo React (Tailwind CSS) enviado para seguir estritamente o design system "Dark Luxury / Technical".

Regras obrigatorias:

1. PALETA DE CORES E FUNDOS
- Fundo principal da aplicacao: `bg-black` (#000000).
- Fundo de cards/containers/modais: `bg-zinc-950` (#09090b).
- Bordas de cards/containers: `border border-zinc-800/60`.
- Texto principal: `text-zinc-100` ou `text-white`.
- Texto secundario (labels, subtitulos): `text-zinc-500` ou `text-zinc-400`.
- Cores de destaque numerico: `text-emerald-400` (positivo/entradas) e `text-rose-400` (negativo/saidas).

2. TIPOGRAFIA
- Fonte padrao para textos: `font-sans` (Inter).
- Fonte obrigatoria para numeros, valores monetarios, datas e codigos: `font-mono` (JetBrains Mono).
- Titulos de secao/card: `text-xs font-semibold text-zinc-500 uppercase tracking-wider`.
- Valores principais (ex.: saldo): `text-3xl font-bold tracking-tight font-mono`.

3. ESTILO DE CARDS E CONTAINERS
- Arredondamento: `rounded-2xl`.
- Padding interno padrao: `p-6`.
- Efeito hover obrigatorio em qualquer container visual principal: adicione `group` no container principal e inclua:

```jsx
<div className="absolute -inset-px bg-gradient-to-b from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl pointer-events-none" />
```

- O container principal deve ter `relative overflow-hidden` para o efeito funcionar.

4. BOTOES E INTERACOES
- Botao primario (acoes principais): `bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2.5 rounded-xl text-sm font-medium transition-colors shadow-lg shadow-emerald-500/20`.
- Botao secundario (cancelar/voltar/filtros): `bg-zinc-900 border border-zinc-800 hover:bg-zinc-800 text-zinc-200 px-4 py-2.5 rounded-xl text-sm font-medium transition-colors`.

5. TABELAS DE DADOS
- Cabecalho: `text-xs font-semibold text-zinc-500 uppercase tracking-wider border-b border-zinc-800/60 pb-3`.
- Linhas: `border-b border-zinc-800/40 hover:bg-zinc-900/50 transition-colors`.
- Valores: sempre usar `font-mono`.

6. INPUTS E FORMULARIOS
- Fundo: `bg-zinc-900`.
- Borda e foco: `border border-zinc-800 focus:border-zinc-600 focus:ring-1 focus:ring-zinc-600`.
- Texto e placeholder: `text-zinc-200 placeholder:text-zinc-600 rounded-xl px-4 py-2.5`.

Requisitos de entrega:
- Mantenha a logica de negocio intacta.
- Altere apenas classes Tailwind e a estrutura HTML/JSX necessaria para atingir o visual.
- Aplique remocao agressiva de classes antigas: elimine classes utilitarias legadas que conflitem ou desviem do design system, mantendo somente o conjunto final coerente com este padrao.
- Retorne:
  1. codigo final refatorado;
  2. resumo curto das alteracoes visuais aplicadas;
  3. lista de pontos onde o estilo nao pode ser aplicado sem mudar regra de negocio (se houver).