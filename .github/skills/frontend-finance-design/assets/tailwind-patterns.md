# Padrões Tailwind CSS

Guia de padrões e boas práticas para usar Tailwind CSS no projeto de gestão financeira.

## Cores Padronizadas

### Entradas (Verde)
```html
<!-- Texto -->
<p class="text-green-600">+R$ 500</p>

<!-- Background -->
<div class="bg-green-50">...</div>

<!-- Border -->
<div class="border-l-4 border-green-500">...</div>

<!-- Botão -->
<button class="bg-green-500 hover:bg-green-600">Entrada</button>
```

### Saídas (Vermelho)
```html
<!-- Texto -->
<p class="text-red-600">-R$ 85,50</p>

<!-- Background -->
<div class="bg-red-50">...</div>

<!-- Border -->
<div class="border-l-4 border-red-500">...</div>

<!-- Botão -->
<button class="bg-red-500 hover:bg-red-600">Saída</button>
```

### Primária (Azul)
```html
<!-- Texto -->
<p class="text-blue-600">Ação Principal</p>

<!-- Background -->
<div class="bg-blue-500">...</div>

<!-- Focus/Hover -->
<button class="focus:ring-2 focus:ring-blue-500">Salvar</button>
```

### Neutras (Cinza)
```html
<!-- Texto secundário -->
<p class="text-gray-600">Informação adicional</p>

<!-- Background -->
<div class="bg-gray-50">...</div>
<div class="bg-white">...</div>

<!-- Borders -->
<div class="border border-gray-300">...</div>
```

## Espaçamento Consistente

### Padding (p-X)
```html
<!-- Pequeno -->
<div class="p-2">Pequeno espaço</div>

<!-- Médio (padrão) -->
<div class="p-4">Espaço médio</div>

<!-- Grande -->
<div class="p-6">Grande espaço</div>

<!-- Horizontal + Vertical -->
<div class="px-4 py-6">Espaço customizado</div>
```

### Margin (m-X)
```html
<!-- Separação entre seções -->
<div class="mb-6">Seção com espaço embaixo</div>

<!-- Espaço entre itens -->
<div class="space-y-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>
```

### Gap (gap-X)
```html
<!-- Espaço em grids -->
<div class="grid grid-cols-2 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<!-- Espaço em flex -->
<div class="flex gap-3">
  <button>Cancelar</button>
  <button>Salvar</button>
</div>
```

## Tipografia

### Tamanhos (text-X)
```html
<!-- Pequeno -->
<p class="text-sm">Texto pequeno (12px)</p>

<!-- Base (padrão) -->
<p class="text-base">Texto normal (16px)</p>

<!-- Grande -->
<p class="text-lg">Texto grande (18px)</p>

<!-- Muito Grande -->
<h1 class="text-4xl">Título principal (36px)</h1>

<!-- Saldo em Destaque -->
<p class="text-5xl">Muito grande (48px)</p>
```

### Peso (font-X)
```html
<!-- Normal -->
<p class="font-normal">Peso normal</p>

<!-- Semi-bold (padrão para labels) -->
<p class="font-semibold">Semi-bold</p>

<!-- Bold (títulos) -->
<h2 class="font-bold">Título em bold</h2>
```

### Combinações Comuns
```html
<!-- Label de seção -->
<p class="text-sm font-semibold text-gray-700">Categoria</p>

<!-- Valor em destaque -->
<p class="text-2xl font-bold text-green-600">+R$ 5.200</p>

<!-- Descrição secundária -->
<p class="text-sm text-gray-500">Alimentação • Ontem</p>
```

## Componentes Reutilizáveis

### Card Padrão
```html
<div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition">
  <h3 class="font-semibold text-gray-900">Título</h3>
  <p class="text-sm text-gray-600">Descrição</p>
</div>
```

### Botão Primário
```html
<button class="w-full md:w-auto px-4 py-2 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-600 transition">
  Salvar
</button>
```

### Botão Secundário
```html
<button class="w-full md:w-auto px-4 py-2 border border-gray-300 text-gray-600 rounded-lg font-semibold hover:bg-gray-50 transition">
  Cancelar
</button>
```

### Input Campo
```html
<input 
  type="text"
  placeholder="Digite aqui"
  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
>
```

### Select Campo
```html
<select class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
  <option>Opção 1</option>
  <option>Opção 2</option>
</select>
```

### Badge/Tag
```html
<!-- Verde (entrada) -->
<span class="inline-block px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
  Entrada
</span>

<!-- Vermelho (saída) -->
<span class="inline-block px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-semibold">
  Saída
</span>
```

### Alerta/Mensagem
```html
<!-- Sucesso -->
<div class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
  ✓ Transação salva com sucesso!
</div>

<!-- Erro -->
<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
  ✗ Erro ao salvar. Tente novamente.
</div>
```

## Responsive Classes

### Breakpoints
- **Base (mobile)**: Sem prefixo (0px)
- **md:** Tablet (768px)
- **lg:** Desktop (1024px)

### Exemplos Comuns
```html
<!-- Grid responsivo -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- 1 coluna mobile, 2 tablet, 3 desktop -->
</div>

<!-- Direção flex responsiva -->
<div class="flex flex-col md:flex-row gap-4">
  <!-- Coluna mobile, linha tablet+ -->
</div>

<!-- Tamanho responsivo -->
<h1 class="text-2xl md:text-3xl lg:text-4xl">Título</h1>

<!-- Visibilidade responsiva -->
<header class="md:hidden">Visível apenas mobile</header>
<aside class="hidden lg:block">Visível apenas desktop</aside>

<!-- Padding responsivo -->
<div class="p-4 md:p-6 lg:p-8">Espaço aumenta em tablets e desktops</div>

<!-- Width responsiva -->
<input class="w-full md:w-1/2 lg:w-1/3">
```

## Estados (Hover, Focus, Active)

### Hover
```html
<button class="bg-blue-500 hover:bg-blue-600 transition">
  Hover muda cor
</button>

<div class="border border-gray-200 hover:shadow-md transition">
  Hover adiciona sombra
</div>
```

### Focus (Acessibilidade)
```html
<input class="focus:ring-2 focus:ring-blue-500 focus:border-transparent">

<button class="focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
  Foco visual claro
</button>
```

### Transition
```html
<!-- Suave -->
<button class="bg-blue-500 hover:bg-blue-600 transition">
  Mudança suave
</button>

<!-- Com duração específica -->
<div class="hover:shadow-lg transition-shadow duration-200">
  Sombra animada
</div>
```

## Gradientes

### Horizontal
```html
<div class="bg-gradient-to-r from-blue-500 to-blue-600">
  Gradiente da esquerda para direita
</div>
```

### Vertical
```html
<div class="bg-gradient-to-b from-blue-500 to-blue-600">
  Gradiente de cima para baixo
</div>
```

## Sombras

### Sem sombra (padrão)
```html
<div class="shadow-none">Sem sombra</div>
```

### Sombra pequena
```html
<div class="shadow-sm">Sombra pequena</div>
```

### Sombra média
```html
<div class="shadow-md">Sombra média</div>
```

### Sombra grande
```html
<div class="shadow-lg">Sombra grande</div>
```

## Border Radius

```html
<!-- Pequeno -->
<div class="rounded">Pequeno arredondamento</div>

<!-- Médio (padrão) -->
<div class="rounded-lg">Arredondamento médio</div>

<!-- Grande -->
<div class="rounded-xl">Arredondamento grande</div>

<!-- Completo (círculo se quadrado) -->
<div class="rounded-full">Círculo</div>
```

## Max Width

```html
<!-- Contenedor principal -->
<div class="max-w-7xl mx-auto">
  Conteúdo centralizado com max width
</div>

<!-- Input com width máximo -->
<input class="max-w-md">
```

## Checklist de Padrões

- [ ] Cores corretas: verde/vermelho/azul
- [ ] Espaçamento consistente: p-4, gap-4, mb-6
- [ ] Tipografia clara: tamanhos e pesos corretos
- [ ] Responsive: grid, flex com breakpoints
- [ ] Estados: hover, focus, transition
- [ ] Sem inline styles (usar classes Tailwind)
- [ ] Sem valores arbitrários
- [ ] Mobile-first (sem prefixo = base mobile)
- [ ] Acessibilidade: focus rings, contrast suficiente
- [ ] Performance: classes reutilizáveis, sem duplicação
