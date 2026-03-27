Atue como um Engenheiro de Frontend Sênior e Especialista em UI/UX. Preciso que você refatore os componentes da minha aplicação React (Tailwind CSS) para seguir estritamente o novo design system "Dark Luxury / Technical" que estabeleci no meu Dashboard.

Aqui estão as diretrizes absolutas de estilo que você DEVE aplicar em todas as telas, modais, formulários e tabelas:

1. PALETA DE CORES E FUNDOS:
- Fundo principal da aplicação: `bg-black` (#000000).
- Fundo de Cards/Containers/Modais: `bg-zinc-950` (#09090b).
- Bordas de Cards/Containers: `border border-zinc-800/60`.
- Texto principal: `text-zinc-100` ou `text-white`.
- Texto secundário (labels, subtítulos): `text-zinc-500` ou `text-zinc-400`.
- Cores de destaque numérico: `text-emerald-400` (Positivo/Entradas) e `text-rose-400` (Negativo/Saídas).

2. TIPOGRAFIA:
- Fonte padrão para textos: `font-sans` (Inter).
- Fonte OBRIGATÓRIA para TODOS os números, valores monetários, datas e códigos: `font-mono` (JetBrains Mono).
- Títulos de seções/cards: Devem ser pequenos, em maiúsculas e com espaçamento: `text-xs font-semibold text-zinc-500 uppercase tracking-wider`.
- Valores principais (ex: saldo do card): `text-3xl font-bold tracking-tight font-mono`.

3. ESTILO DE CARDS E CONTAINERS:
- Arredondamento: `rounded-2xl`.
- Padding interno padrão: `p-6`.
- Efeito Hover (Obrigatório em cards interativos): Adicione a classe `group` no container principal e inclua este elemento absoluto dentro dele para criar um brilho sutil:
  `<div className="absolute -inset-px bg-gradient-to-b from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-2xl pointer-events-none" />`
- O container principal deve ter `relative overflow-hidden` para o efeito acima funcionar.

4. BOTÕES E INTERAÇÕES:
- Botão Primário (Ações principais como "Salvar", "Nova Transação"): `bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2.5 rounded-xl text-sm font-medium transition-colors shadow-lg shadow-emerald-500/20`.
- Botão Secundário (Cancelar, Voltar, Filtros): `bg-zinc-900 border border-zinc-800 hover:bg-zinc-800 text-zinc-200 px-4 py-2.5 rounded-xl text-sm font-medium transition-colors`.

5. TABELAS DE DADOS (Ex: Lista de Transações):
- Cabeçalho da tabela: `text-xs font-semibold text-zinc-500 uppercase tracking-wider border-b border-zinc-800/60 pb-3`.
- Linhas da tabela: `border-b border-zinc-800/40 hover:bg-zinc-900/50 transition-colors`.
- Valores na tabela: Sempre usar `font-mono`.

6. INPUTS E FORMULÁRIOS:
- Fundo do input: `bg-zinc-900`.
- Borda do input: `border border-zinc-800 focus:border-zinc-600 focus:ring-1 focus:ring-zinc-600`.
- Texto do input: `text-zinc-200 placeholder:text-zinc-600 rounded-xl px-4 py-2.5`.

Por favor, analise o código que vou enviar a seguir e reescreva-o aplicando rigorosamente todas essas regras de design. Mantenha a lógica de negócio intacta, altere apenas as classes do Tailwind e a estrutura HTML necessária para atingir esse visual.