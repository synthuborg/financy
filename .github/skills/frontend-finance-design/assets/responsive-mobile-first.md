# Mobile-First Responsividade

Guia para garantir que a interface é verdadeiramente mobile-first com responsividade perfeita em todos os tamanhos.

## Princípio Mobile-First

**Mobile-first significa:**
1. Começar SEMPRE sem breakpoints (mobile)
2. Adicionar `md:` e `lg:` conforme necessário
3. Nunca esconder features cruciais em mobile
4. Layout mobile é a BASE, desktop é a exceção

### ✓ Correto - Mobile First
```html
<!-- Espaço padrão (mobile) -->
<div class="p-4">Padding padrão</div>

<!-- Em tablet, aumenta espaço -->
<div class="p-4 md:p-6">Padding adaptativo</div>

<!-- Em desktop, ainda maior -->
<div class="p-4 md:p-6 lg:p-8">Padding totalmente responsivo</div>
```

### ✗ Incorreto - Desktop First
```html
<!-- Desktop é a "base" (errado!) -->
<div class="p-8 md:p-6 lg:p-4">
  <!-- Mobile fica pequeno, confuso -->
</div>

<!-- Ou pior, esconde features -->
<div class="hidden md:block">
  <!-- Recurso essencial desaparece em mobile -->
</div>
```

## Breakpoints Tailwind

| Prefixo | Largura | Dispositivo |
|---------|---------|-------------|
| (none)  | 0px+    | Mobile (padrão) |
| `sm:`   | 640px   | Celular grande |
| `md:`   | 768px   | Tablet |
| `lg:`   | 1024px  | Desktop |
| `xl:`   | 1280px  | Desktop grande |
| `2xl:`  | 1536px  | Super grande |

## Padrões de Grid Responsivos

### 1. Coluna Única → 2 Colunas → 3 Colunas

```html
<!-- Mobile: 1 coluna, Tablet: 2, Desktop: 3 -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
  <div>Card 4</div>
  <div>Card 5</div>
  <div>Card 6</div>
</div>

<!-- Resultado:
  Mobile (0-767px):
  [Card 1]
  [Card 2]
  [Card 3]
  [Card 4]
  [Card 5]
  [Card 6]

  Tablet (768-1023px):
  [Card 1] [Card 2]
  [Card 3] [Card 4]
  [Card 5] [Card 6]

  Desktop (1024px+):
  [Card 1] [Card 2] [Card 3]
  [Card 4] [Card 5] [Card 6]
-->
```

### 2. 2 Colunas → 3 Colunas

```html
<!-- Mobile: 2 colunas, Desktop: 3 -->
<div class="grid grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- Resumo cards: Entradas, Saídas, Saldo -->
</div>
```

### 3. Coluna Dupla → Versão Cheia

```html
<!-- Um item (full width mobile), outros em grid -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
  <div class="col-span-1 md:col-span-2">
    <!-- Saldo: full em mobile, 2 cols em tablet+ -->
  </div>
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

## Padrões de Flex Responsivos

### 1. Coluna → Linha

```html
<!-- Mobile: vertical, Tablet+: horizontal -->
<div class="flex flex-col md:flex-row gap-4">
  <button class="flex-1">Entrada</button>
  <button class="flex-1">Saída</button>
</div>
```

### 2. Alinhamento Adaptativo

```html
<!-- Mobile: center, Desktop: space-between -->
<div class="flex flex-col md:flex-row items-center md:items-start justify-between gap-4">
  <div>Esquerda</div>
  <div>Direita</div>
</div>
```

### 3. Wrap em Linha

```html
<!-- Items quebram em múltiplas linhas -->
<div class="flex flex-wrap gap-2">
  <span class="inline-block px-3 py-1 bg-gray-200 rounded">Tag 1</span>
  <span class="inline-block px-3 py-1 bg-gray-200 rounded">Tag 2</span>
  <span class="inline-block px-3 py-1 bg-gray-200 rounded">Tag 3</span>
</div>
```

## Layout Global (Dashboard Completo)

### Estrutura Base

```html
<!-- Topbar (mobile + tablet) -->
<header class="sticky top-0 md:hidden bg-white shadow-sm">
  <!-- Navegação mobile -->
</header>

<!-- Sidebar (desktop only) -->
<aside class="hidden lg:block fixed left-0 top-0 w-64 h-screen bg-gray-900">
  <!-- Navegação desktop -->
</aside>

<!-- Main (responsiva) -->
<main class="lg:ml-64 '' mx-auto px-4 md:px-6 lg:px-8 py-6">
  <!-- Conteúdo adaptativo -->
</main>
```

### Componentes Comuns

#### Saldo em Destaque
```html
<!-- Sempre full width -->
<section class="bg-blue-600 text-white rounded-lg p-6">
  <p class="text-sm opacity-90">Saldo Atual</p>
  <h1 class="text-4xl md:text-5xl font-bold">R$ 2.450,50</h1>
</section>
```

#### Cards de Resumo
```html
<!-- Mobile: 2 colunas, Tablet: 3 colunas -->
<div class="grid grid-cols-2 md:grid-cols-3 gap-4">
  <div class="bg-white p-4 rounded-lg">Entradas</div>
  <div class="bg-white p-4 rounded-lg">Saídas</div>
  <div class="col-span-2 md:col-span-1 bg-white p-4 rounded-lg">
    Saldo do Mês
  </div>
</div>
```

#### Lista de Transações
```html
<!-- Full width em todos os tamanhos -->
<ul class="space-y-2">
  <li class="bg-white p-4 md:p-6 rounded-lg">
    <div class="flex flex-col md:flex-row justify-between">
      <div>
        <h3 class="font-semibold">Transação</h3>
        <p class="text-sm text-gray-600">Descrição</p>
      </div>
      <p class="text-lg font-bold text-red-600 mt-2 md:mt-0">-R$ 50</p>
    </div>
  </li>
</ul>
```

#### Formulário
```html
<!-- Mobile: full width, Desktop: 2 colunas -->
<form class="grid grid-cols-1 md:grid-cols-2 gap-4">
  <div class="md:col-span-2">
    <label>Tipo</label>
    <select class="w-full ..."><!-- opções --></select>
  </div>
  
  <div class="md:col-span-2">
    <label>Valor</label>
    <input type="number" class="w-full ...">
  </div>
  
  <div>
    <label>Categoria</label>
    <select class="w-full ..."><!-- opções --></select>
  </div>
  
  <div>
    <label>Data</label>
    <input type="date" class="w-full ...">
  </div>
  
  <div class="md:col-span-2 flex gap-2">
    <button type="reset" class="flex-1">Cancelar</button>
    <button type="submit" class="flex-1">Salvar</button>
  </div>
</form>
```

## Visibilidade Responsiva

### Mostrar/Esconder por Tamanho

```html
<!-- Topbar: visível apenas em mobile/tablet -->
<header class="md:hidden">
  <!-- Topbar content -->
</header>

<!-- Sidebar: visível apenas em desktop -->
<aside class="hidden lg:block">
  <!-- Sidebar content -->
</aside>

<!-- Elemento que muda de visibilidade -->
<div class="block md:hidden">Apenas mobile</div>
<div class="hidden md:block">Apenas tablet+</div>
<div class="hidden lg:block">Apenas desktop</div>
```

### Padrão: "Mobile Menu → Desktop Nav"

```html
<!-- Hambúrguer (mobile) -->
<button id="mobileMenuBtn" class="md:hidden">
  ☰ Menu
</button>

<!-- Menu Completo (desktop + mobile expandido) -->
<nav id="mobileMenu" class="hidden md:block md:static">
  <ul>
    <li><a href="/">Dashboard</a></li>
    <li><a href="/transactions">Transações</a></li>
  </ul>
</nav>

<script>
  mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
  });
</script>
```

## Tamanho de Fonte Responsivo

```html
<!-- Pequeno em mobile, maior em desktop -->
<h1 class="text-2xl md:text-3xl lg:text-4xl">Título</h1>

<!-- Valores -->
<p class="text-3xl md:text-4xl font-bold">R$ 2.450</p>

<!-- Texto normal -->
<p class="text-sm md:text-base">Descrição</p>
```

## Padding/Margin Responsivo

```html
<!-- Mobile: p-4, Tablet: p-6, Desktop: p-8 -->
<main class="p-4 md:p-6 lg:p-8">
  <!-- Conteúdo -->
</main>

<!-- Gap responsivo em grids -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
  <!-- Com espaço maior em tablets+ -->
</div>
```

## Width Responsivo

```html
<!-- Full em mobile, reduzido em desktop -->
<div class="w-full md:w-3/4 lg:w-2/3">
  <!-- Conteúdo que respira melhor em desktop -->
</div>

<!-- Input field -->
<input class="w-full md:w-1/2 lg:w-1/3">
```

## Testes de Responsividade

### 1. Chrome DevTools
```
1. Abra DevTools (F12)
2. Clique em "Toggle device toolbar" (Ctrl+Shift+M)
3. Teste dispositivos:
   - iPhone SE (375px)
   - iPhone 12 (390px)
   - Pixel 5 (412px)
   - iPad (768px)
   - Desktop (1920px)

Verificar:
- [ ] Sem scroll horizontal
- [ ] Texto legível (16px+)
- [ ] Botões clicáveis (44px+)
- [ ] Layout não quebra
```

### 2. Dispositivos Reais
```
1. Teste em iPhone real (se possível)
2. Teste em Android real
3. Teste em landscape (girar dispositivo)

Verificar:
- [ ] Tudo funciona
- [ ] Teclado não esconde input importante
- [ ] Modal fecha bem
```

### 3. Breakpoints
```
Abrir a página em:
- [ ] 375px (mobile small)
- [ ] 768px (tablet)
- [ ] 1024px (desktop)
- [ ] 1920px (desktop grande)

Em cada breakpoint:
- [ ] Verificar se layout muda conforme esperado
- [ ] Verificar se nenhuma feature desaparece
```

## Exemplo Completo: Dashboard Responsivo

```html
<main class="lg:ml-64 '' mx-auto px-4 py-6">
  
  <!-- Seção 1: Saldo -->
  <section class="bg-blue-600 text-white rounded-lg p-6 mb-6">
    <p class="text-sm opacity-90">Saldo Atual</p>
    <h1 class="text-4xl md:text-5xl font-bold">R$ 2.450,50</h1>
  </section>

  <!-- Seção 2: Cards -->
  <section class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
    <div class="bg-white p-4 rounded-lg border">
      <p class="text-sm text-gray-600">Entradas</p>
      <p class="text-2xl font-bold text-green-600">+R$ 5.200</p>
    </div>
    <div class="bg-white p-4 rounded-lg border">
      <p class="text-sm text-gray-600">Saídas</p>
      <p class="text-2xl font-bold text-red-600">-R$ 2.750</p>
    </div>
    <div class="col-span-2 md:col-span-1 bg-white p-4 rounded-lg border">
      <p class="text-sm text-gray-600">Saldo Mês</p>
      <p class="text-2xl font-bold text-blue-600">+R$ 2.450</p>
    </div>
  </section>

  <!-- Seção 3: Filtros -->
  <section class="bg-white p-4 rounded-lg border mb-6">
    <div class="flex flex-col md:flex-row gap-3">
      <select class="flex-1">
        <option>Todos os meses</option>
      </select>
      <select class="flex-1">
        <option>Todas as categorias</option>
      </select>
      <button class="md:w-auto px-4">Limpar</button>
    </div>
  </section>

  <!-- Seção 4: Transações -->
  <section>
    <h3 class="text-lg font-bold mb-4">Recentes</h3>
    <ul class="space-y-2">
      <li class="bg-white p-4 md:p-6 rounded-lg border">
        <div class="flex flex-col md:flex-row justify-between">
          <div>
            <h4 class="font-semibold">Supermercado</h4>
            <p class="text-sm text-gray-600">Alimentação • Ontem</p>
          </div>
          <p class="text-lg font-bold text-red-600">-R$ 85,50</p>
        </div>
      </li>
    </ul>
  </section>

</main>
```

## Checklist Mobile-First

- [ ] Começar sempre SEM breakpoints (mobile é base)
- [ ] Adicionar `md:` para tablet
- [ ] Adicionar `lg:` para desktop
- [ ] Sem scroll horizontal em nenhum tamanho
- [ ] Texto mínimo 16px em mobile
- [ ] Botões mínimo 44px x 44px
- [ ] Topbar sticky em mobile
- [ ] Sidebar escondida em mobile
- [ ] FAB sempre acessível
- [ ] Modal funciona em mobile (não corta)
- [ ] Imagens responsivas
- [ ] Testar em DevTools (iPhone SE, Pixel 5, iPad, Desktop)
- [ ] Testar em dispositivo real
- [ ] Testar em landscape
- [ ] Nenhuma feature desaparece em mobile
