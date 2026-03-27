---
name: frontend-finance-design
description: 'UI/UX design for personal finance dashboard. Premium dark mode, mobile-first, Tailwind CSS. Use when: building financial UI, dark layouts, responsive components, or styling with Tailwind.'
argument-hint: 'Leave empty or specify: "dashboard", "mobile", "tailwind", "dark", "components"'
---

# Frontend Finance Design System

Sistema de design **premium dark mode** para interface de gestão financeira pessoal. Dark-first, mobile-first, minimalista e com foco total em clareza e sofisticação visual.

## Princípios Fundamentais

### 1. Dark-First (OBRIGATÓRIO)
- A aplicação é nativamente escura — sem flash de branco ou fundo claro
- Fundo base: `bg-slate-900` (#0F172A) — azul-acinzentado escuro, não preto puro
- Superfícies elevadas (cards, modais): `bg-slate-800` (#1E293B)
- Nunca usar `bg-white` ou `bg-gray-*` como fundo principal

### 2. Mobile-First Absoluto
- Estilo base sem breakpoints = mobile (375px) primeiro
- Layout vertical e simples
- Elementos grandes e clicáveis (mínimo 44px de altura)
- Usar `sm:`, `md:`, `lg:` apenas para expandir para telas maiores

### 3. Minimalismo Premium
- Espaçamento generoso (`p-6`, `gap-6`) para dar "respiro" aos elementos
- Sem bordas desnecessárias — quando usar, sempre sutis: `border border-slate-700/50`
- Sombras sutis para hierarquia: `shadow-xl`
- Apenas o necessário em tela

### 4. UX Centrada no Usuário
- Linguagem simples: "Entradas", "Saídas", "Saldo"
- Feedback imediato em todas as ações
- Controle total: editar, filtrar, visualizar facilmente
- Zero fricção: menos cliques, menos formulários

### 5. Tipografia Clara
- Fonte sans-serif moderna (Inter, Roboto ou Geist via CDN)
- Texto principal: `text-slate-50` — alto contraste
- Texto secundário: `text-slate-400` — labels, descrições
- Hierarquia forte: `text-3xl font-bold` para valores, `text-sm` para rótulos

### 6. HTML Limpo (CRÍTICO)
- Semântico: `<header>`, `<main>`, `<section>`
- Sem divs em excesso
- Estrutura reutilizável
- Fácil de manter

## Paleta de Cores — Premium Dark

| Papel | Classe Tailwind | Hex | Uso |
|-------|----------------|-----|-----|
| Fundo | `bg-slate-900` | #0F172A | Fundo de toda a página |
| Superfície | `bg-slate-800` | #1E293B | Cards, modais, inputs |
| Borda | `border-slate-700` | #334155 | Divisores sutis |
| Texto principal | `text-slate-50` | #F8FAFC | Títulos, valores |
| Texto secundário | `text-slate-400` | #94A3B8 | Labels, descrições |
| Destaque (Accent) | `text-sky-400` / `bg-sky-400` | #38BDF8 | Botão CTA, links ativos, foco |
| Alternativo Accent | `text-indigo-400` / `bg-indigo-400` | #818CF8 | Opcional, uso moderado |
| Sucesso / Entrada | `text-green-400` | #4ADE80 | Receitas, valores positivos |
| Alerta / Saída | `text-red-400` | #F87171 | Despesas, valores negativos |

> **Regra:** use a cor de Destaque (`sky-400`) com moderação — apenas para CTA e estado ativo.

## Quando Usar Esta Skill

1. **Criar Dashboard**: Layout dark, saldo, cards, transações
2. **Componentes**: Modais, cards, listas dark
3. **Responsividade**: Garantir mobile-first no dark mode
4. **Tailwind Pattern**: Classes corretas da paleta escura
5. **UX Check**: Validar clareza e feedback
6. **HTML Refactor**: Limpar estrutura

## Procedimento Rápido

### 1. Estrutura Global (Sempre)

Use [padrão de layout principal](./assets/dashboard-template.html):

```html
<!-- Fundo base: slate-900 em todo o body -->
<body class="bg-slate-900 text-slate-50 min-h-screen">

  <!-- Topbar (mobile + tablet) -->
  <header class="sticky top-0 bg-slate-800 border-b border-slate-700/50 md:hidden">
    <!-- Conteúdo da topbar -->
  </header>

  <!-- Sidebar (apenas desktop) -->
  <aside class="hidden lg:flex fixed left-0 top-0 w-64 h-screen
                bg-slate-800 border-r border-slate-700/50 flex-col">
    <!-- Navegação fixa -->
  </aside>

  <!-- Main Content -->
  <main class="lg:ml-64 '' mx-auto px-4 py-6">
    <!-- Dashboard, páginas, etc -->
  </main>

</body>
```

### 2. Dashboard Components

**Saldo em Destaque** (sempre visível):
```html
<!-- Card de saldo — superfície elevada com destaque no valor -->
<section class="bg-slate-800 rounded-2xl shadow-xl border border-slate-700/50 p-6">
  <p class="text-sm text-slate-400 mb-1">Saldo Atual</p>
  <h1 class="text-4xl font-bold text-slate-50">R$ 2.450,50</h1>
  <p class="text-xs text-slate-400 mt-2">Atualizado agora</p>
</section>
```

**Cards de Resumo**:
```html
<div class="grid grid-cols-2 md:grid-cols-3 gap-4">
  <!-- Entrada -->
  <div class="bg-slate-800 rounded-2xl shadow-xl border border-slate-700/50 p-4">
    <p class="text-xs text-slate-400 mb-1">Entradas</p>
    <p class="text-2xl font-bold text-green-400">+R$ 5.200</p>
  </div>
  <!-- Saída -->
  <div class="bg-slate-800 rounded-2xl shadow-xl border border-slate-700/50 p-4">
    <p class="text-xs text-slate-400 mb-1">Saídas</p>
    <p class="text-2xl font-bold text-red-400">-R$ 2.750</p>
  </div>
</div>
```

### 3. Mobile-First Responsividade

Sempre começar sem breakpoints, adicionar `md:` e `lg:` conforme necessário:

```html
<!-- Mobile: 1 coluna, Tablet: 2 colunas, Desktop: 3 colunas -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Cards -->
</div>
```

Ver [guia completo de responsive](./assets/responsive-mobile-first.md)

### 4. Formulário Adicionar Transação (Modal)

```html
<!-- Modal dark -->
<div id="modalTransacao" class="hidden fixed inset-0 bg-black/70 z-50
                              flex items-center justify-center p-4">
  <div class="bg-slate-800 rounded-2xl shadow-xl border border-slate-700/50
              max-w-md w-full p-6">
    <h2 class="text-xl font-bold text-slate-50 mb-6">Nova Transação</h2>

    <form class="space-y-4">
      <!-- Tipo (entrada/saída) -->
      <div>
        <label class="block text-sm text-slate-400 mb-2">Tipo</label>
        <div class="flex gap-2">
          <!-- Botão primário ativo -->
          <button type="button"
                  class="flex-1 py-2 px-4 rounded-lg bg-sky-400 text-slate-900
                         font-semibold hover:brightness-110 transition">
            Entrada
          </button>
          <!-- Botão secundário -->
          <button type="button"
                  class="flex-1 py-2 px-4 rounded-lg border border-slate-400
                         text-slate-50 hover:bg-slate-700 transition">
            Saída
          </button>
        </div>
      </div>

      <!-- Valor (campo principal) -->
      <div>
        <label class="block text-sm text-slate-400 mb-2">Valor</label>
        <input type="number" placeholder="0,00" autofocus
               class="w-full px-4 py-3 text-2xl font-bold rounded-lg
                      bg-slate-800 border border-slate-700 text-slate-50
                      placeholder:text-slate-600
                      focus:outline-none focus:border-sky-400 transition">
      </div>

      <!-- Categoria -->
      <div>
        <label class="block text-sm text-slate-400 mb-2">Categoria</label>
        <select class="w-full px-4 py-2 rounded-lg bg-slate-800 border border-slate-700
                       text-slate-50 focus:outline-none focus:border-sky-400 transition">
          <option>Alimentação</option>
          <option>Transporte</option>
          <option>Saúde</option>
        </select>
      </div>

      <!-- Data -->
      <div>
        <label class="block text-sm text-slate-400 mb-2">Data</label>
        <input type="date"
               class="w-full px-4 py-2 rounded-lg bg-slate-800 border border-slate-700
                      text-slate-50 focus:outline-none focus:border-sky-400 transition">
      </div>

      <!-- Descrição (opcional) -->
      <div>
        <label class="block text-sm text-slate-400 mb-2">Descrição (opcional)</label>
        <input type="text" placeholder="Ex: Almocei na pizzaria"
               class="w-full px-4 py-2 rounded-lg bg-slate-800 border border-slate-700
                      text-slate-50 placeholder:text-slate-600
                      focus:outline-none focus:border-sky-400 transition">
      </div>

      <!-- Ações -->
      <div class="flex gap-2 pt-2">
        <button type="button"
                class="flex-1 py-2 px-4 rounded-lg border border-slate-400
                       text-slate-50 hover:bg-slate-700 transition">
          Cancelar
        </button>
        <button type="submit"
                class="flex-1 py-2 px-4 rounded-lg bg-sky-400 text-slate-900
                       font-semibold hover:brightness-110 transition">
          Salvar
        </button>
      </div>
    </form>
  </div>
</div>

<!-- FAB (Floating Action Button) -->
<button class="fixed bottom-6 right-6 w-14 h-14 bg-sky-400 text-slate-900
               rounded-full shadow-xl hover:brightness-110 transition
               flex items-center justify-center">
  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M12 4v16m8-8H4"></path>
  </svg>
</button>
```

### 5. Lista de Transações

```html
<section>
  <h2 class="text-lg font-bold text-slate-50 mb-4">Transações Recentes</h2>

  <div class="space-y-2">
    <!-- Item de transação (saída) -->
    <div class="flex items-center justify-between p-4
                bg-slate-800 rounded-2xl border border-slate-700/50
                hover:bg-slate-700/60 transition">
      <div>
        <p class="font-semibold text-slate-50">Supermercado</p>
        <p class="text-sm text-slate-400">Alimentação • Ontem</p>
      </div>
      <p class="text-lg font-bold text-red-400">-R$ 85,50</p>
    </div>

    <!-- Item de transação (entrada) -->
    <div class="flex items-center justify-between p-4
                bg-slate-800 rounded-2xl border border-slate-700/50
                hover:bg-slate-700/60 transition">
      <div>
        <p class="font-semibold text-slate-50">Salário</p>
        <p class="text-sm text-slate-400">Renda • 01/03</p>
      </div>
      <p class="text-lg font-bold text-green-400">+R$ 3.500,00</p>
    </div>
  </div>
</section>
```

### 6. Filtros

```html
<!-- Usar HTMX: sem onchange JS, ver @htmx-patterns -->
<section class="flex flex-col md:flex-row gap-3 mb-6">
  <!-- Filtro Mês -->
  <select class="flex-1 px-4 py-2 rounded-lg bg-slate-800 border border-slate-700
                 text-slate-50 focus:outline-none focus:border-sky-400 transition"
          hx-get="{% url 'transactions:filter' %}"
          hx-trigger="change"
          hx-target="#transaction-list"
          name="mes">
    <option value="">Todos os meses</option>
    <option value="01">Janeiro</option>
    <option value="03" selected>Março</option>
  </select>

  <!-- Filtro Categoria -->
  <select class="flex-1 px-4 py-2 rounded-lg bg-slate-800 border border-slate-700
                 text-slate-50 focus:outline-none focus:border-sky-400 transition"
          hx-get="{% url 'transactions:filter' %}"
          hx-trigger="change"
          hx-target="#transaction-list"
          name="categoria">
    <option value="">Todas as categorias</option>
    <option value="alimentacao">Alimentação</option>
    <option value="transporte">Transporte</option>
  </select>
</section>
```

## Padrões Tailwind

Ver [guia de classes Tailwind](./assets/tailwind-patterns.md) para:
- Espaçamento consistente
- Tipografia
- Cores e gradientes
- Responsive classes
- Estados (hover, focus, active)

## HTML Limpo

Ver [padrões HTML semântico](./assets/html-clean-patterns.md) para:
- Estrutura semântica
- Sem divs desnecessárias
- Componentes reutilizáveis
- Acessibilidade

## Mobile-First Grid

Ver [guia de responsividade](./assets/responsive-mobile-first.md) para:
- Breakpoints: `md:` (768px), `lg:` (1024px)
- Grid responsivo
- Exemplo: 1 col → 2 colunas → 3 colunas

## UX Checklist

Validar com [checklist de UX](./assets/ux-checklist.md):
- [ ] Usuário entende saldo em 1 segundo
- [ ] Adicionar gasto em < 5 segundos
- [ ] Feedback visual imediato
- [ ] Mobile perfeito
- [ ] Sem fricção

## Exemplo: Dashboard Completo

Veja [dashboard-template.html](./assets/dashboard-template.html) para implementação full do dashboard com:
- Topbar responsivo
- Cards de saldo
- Lista de transações
- Filtros
- Modal para adicionar transação
- FAB button

## Padrões de UI — Referência Rápida

### Card (padrão)
```html
<div class="bg-slate-800 p-6 rounded-2xl shadow-xl border border-slate-700/50">
  <!-- conteúdo -->
</div>
```

### Botão Primário (CTA)
```html
<button class="px-6 py-2 rounded-lg bg-sky-400 text-slate-900 font-semibold
               hover:brightness-110 transition">
  Ação Principal
</button>
```

### Botão Secundário
```html
<button class="px-6 py-2 rounded-lg border border-slate-400
               text-slate-50 hover:bg-slate-700 transition">
  Ação Secundária
</button>
```

### Input / Select
```html
<input class="w-full px-4 py-2 rounded-lg bg-slate-800 border border-slate-700
              text-slate-50 placeholder:text-slate-600
              focus:outline-none focus:border-sky-400 transition">
```

### Label de campo
```html
<label class="block text-sm text-slate-400 mb-2">Nome do Campo</label>
```

### Divisor
```html
<hr class="border-slate-700/50">
```

## Checklist de Implementação

- [ ] `body` tem `bg-slate-900 text-slate-50`
- [ ] Nenhum `bg-white` ou `bg-gray-*` no layout
- [ ] Cards usam `bg-slate-800 rounded-2xl shadow-xl border border-slate-700/50`
- [ ] Texto principal `text-slate-50`, secundário `text-slate-400`
- [ ] Entradas em `text-green-400`, saídas em `text-red-400`
- [ ] Botão CTA usa `bg-sky-400 text-slate-900`
- [ ] Inputs com `bg-slate-800 border-slate-700 focus:border-sky-400`
- [ ] Layout segue mobile-first (base → `md:` → `lg:`)
- [ ] HTML semântico (`header`, `main`, `section`)
- [ ] Sem inline styles, sem `onchange` / `onclick` (usar HTMX)
- [ ] Testado em mobile (375px), tablet, desktop
- [ ] FAB acessível e visível
- [ ] Saldo visível em 1 segundo

## Recursos

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Flowbite Components](https://flowbite.com/docs/components/modal/)
- [Mobile-First Design](https://www.uxpin.com/studio/blog/mobile-first-design/)
- [Semantic HTML](https://developer.mozilla.org/en-US/docs/Glossary/Semantics)
