# HTML Limpo e Semântico

Padrões de HTML limpo, semântico e reutilizável para o projeto de gestão financeira.

## Princípios

1. **Semântico**: Use tags HTML corretas (`<header>`, `<main>`, `<section>`, etc)
2. **Curto**: Sem aninhamento desnecessário de divs
3. **Reutilizável**: Componentes que podem ser usados em múltiplos lugares
4. **Acessível**: Estrutura que funciona  com leitores de tela

## Estrutura Global

### ✓ Correto
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gestão Financeira</title>
</head>
<body>
  
  <!-- Navegação (mobile) -->
  <header class="sticky top-0 bg-white shadow-sm">
    <nav><!-- conteúdo --></nav>
  </header>

  <!-- Navegação (desktop) -->
  <aside class="hidden lg:block">
    <nav><!-- conteúdo --></nav>
  </aside>

  <!-- Conteúdo Principal -->
  <main class="max-w-7xl mx-auto">
    <section><!-- dashboard --></section>
    <section><!-- transações --></section>
  </main>

</body>
</html>
```

### ✗ Incorreto
```html
<!-- Muitos divs, sem semântica -->
<div class="app">
  <div class="container">
    <div class="header">
      <div class="nav-wrapper">
        <div class="nav-items">
          <div class="nav-item">item</div>
          <div class="nav-item">item</div>
        </div>
      </div>
    </div>
    <div class="content">
      <div class="section-wrapper">
        <div class="section-content">
          <!-- conteúdo aninhado demais -->
        </div>
      </div>
    </div>
  </div>
</div>
```

## Componentes Reutilizáveis

### Card de Transação

#### ✓ Correto
```html
<article class="bg-white p-4 rounded-lg border border-gray-200">
  <div class="flex items-center justify-between">
    <div>
      <h3 class="font-semibold">Supermercado</h3>
      <p class="text-sm text-gray-600">Alimentação • Ontem</p>
    </div>
    <p class="text-lg font-bold text-red-600">-R$ 85,50</p>
  </div>
</article>
```

#### ✗ Incorreto
```html
<!-- Divs em excesso, falta de semântica -->
<div class="card">
  <div class="card-content">
    <div class="card-left">
      <div class="card-title">Supermercado</div>
      <div class="card-meta">
        <div class="category">Alimentação</div>
        <div class="date">Ontem</div>
      </div>
    </div>
    <div class="card-right">
      <div class="card-amount">-R$ 85,50</div>
    </div>
  </div>
</div>
```

### Card de Resumo

#### ✓ Correto
```html
<article class="bg-white p-4 rounded-lg border border-gray-200">
  <p class="text-sm text-gray-600">Entradas</p>
  <p class="text-2xl font-bold text-green-600">+R$ 5.200</p>
</article>
```

#### ✗ Incorreto
```html
<div class="summary-card">
  <div class="summary-label">
    <span class="label-text">Entradas</span>
  </div>
  <div class="summary-value">
    <span class="value-formatter">+R$ 5.200</span>
  </div>
</div>
```

### Lista de Itens

#### ✓ Correto
```html
<ul class="space-y-2">
  <li class="bg-white p-4 rounded-lg border border-gray-200">
    <div class="flex justify-between">
      <div>
        <strong>Item</strong>
        <p class="text-sm text-gray-600">Descrição</p>
      </div>
      <span class="text-lg font-bold">Valor</span>
    </div>
  </li>
  <li class="bg-white p-4 rounded-lg border border-gray-200">
    <!-- outro item -->
  </li>
</ul>
```

#### ✗ Incorreto
```html
<!-- Div para cada item, sem semântica de lista -->
<div class="items-container">
  <div class="item-wrapper">
    <div class="item">
      <div class="item-title">Item</div>
      <div class="item-description">Descrição</div>
      <div class="item-value">Valor</div>
    </div>
  </div>
</div>
```

### Formulário

#### ✓ Correto
```html
<form>
  <fieldset>
    <legend>Dados Básicos</legend>
    
    <div class="mb-4">
      <label for="tipo" class="block text-sm font-semibold mb-2">
        Tipo
      </label>
      <select id="tipo" name="tipo" class="w-full px-4 py-2 border rounded-lg">
        <option value="">Selecionar</option>
        <option value="entrada">Entrada</option>
        <option value="saida">Saída</option>
      </select>
    </div>

    <div class="mb-4">
      <label for="valor" class="block text-sm font-semibold mb-2">
        Valor
      </label>
      <input 
        id="valor"
        type="number"
        name="valor"
        placeholder="0,00"
        step="0.01"
        required
        class="w-full px-4 py-2 border rounded-lg"
      >
    </div>
  </fieldset>

  <div class="flex gap-2">
    <button type="reset" class="px-4 py-2 border rounded-lg">
      Limpar
    </button>
    <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-lg">
      Salvar
    </button>
  </div>
</form>
```

#### ✗ Incorreto
```html
<!-- Sem labels estruturadas, sem fieldset -->
<form>
  <div class="form-group">
    <div>Tipo</div>
    <select>
      <option>Entrada</option>
      <option>Saída</option>
    </select>
  </div>

  <div class="form-group">
    <div>Valor</div>
    <input type="number" placeholder="0,00">
  </div>

  <div>
    <button>Salvar</button>
  </div>
</form>
```

### Modal

#### ✓ Correto
```html
<dialog id="modalTransacao" class="w-full max-w-md backdrop:bg-black backdrop:bg-opacity-50 rounded-lg">
  <div class="border-b px-6 py-4">
    <h2 class="text-xl font-bold">Nova Transação</h2>
  </div>

  <form class="p-6">
    <!-- campos do formulário -->
  </form>

  <div class="border-t px-6 py-4 flex gap-2">
    <button form="formTransacao" type="reset" class="flex-1 px-4 py-2 border rounded-lg">
      Cancelar
    </button>
    <button form="formTransacao" type="submit" class="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg">
      Salvar
    </button>
  </div>
</dialog>

<script>
  // Abrir modal
  document.getElementById('btnAdicionar').addEventListener('click', () => {
    document.getElementById('modalTransacao').showModal();
  });

  // Fechar modal
  document.getElementById('modalTransacao').addEventListener('close', () => {
    console.log('Modal fechado');
  });
</script>
```

#### ✗ Incorreto
```html
<!-- Div simulando modal, sem semântica -->
<div id="modal" class="hidden fixed inset-0">
  <div class="bg-white rounded-lg">
    <div class="header">
      <span>Nova Transação</span>
      <button onclick="fecharModal()">X</button>
    </div>
    <div class="body">
      <!-- campos -->
    </div>
    <div class="footer">
      <button onclick="salvar()">Salvar</button>
    </div>
  </div>
</div>
```

## Padrões de Navegação

### Topbar (Mobile + Tablet)

#### ✓ Correto
```html
<header class="sticky top-0 bg-white shadow-sm md:hidden">
  <nav class="max-w-7xl mx-auto px-4 py-4">
    <button aria-label="Menu" class="p-2">
      <svg><!-- ícone --></svg>
    </button>
    <h1 class="text-lg font-bold">Meu Dinheiro</h1>
  </nav>
</header>
```

### Sidebar (Desktop)

#### ✓ Correto
```html
<aside class="hidden lg:block fixed left-0 top-0 w-64 bg-gray-900">
  <nav class="p-6">
    <ul class="space-y-2">
      <li>
        <a href="/" class="block px-4 py-2 rounded-lg">
          Dashboard
        </a>
      </li>
      <li>
        <a href="/transacoes" class="block px-4 py-2 rounded-lg">
          Transações
        </a>
      </li>
    </ul>
  </nav>
</aside>
```

## Acessibilidade

### Atributos Essenciais

```html
<!-- Alt text para imagens -->
<img src="icon.svg" alt="Ícone de entrada">

<!-- Labels para inputs -->
<label for="valor">Valor</label>
<input id="valor" type="number">

<!-- ARIA para elementos dinâmicos -->
<div aria-live="polite" aria-label="Mensagem de status">
  Transação salva com sucesso!
</div>

<!-- Botões com significado -->
<button aria-label="Adicionar transação" class="p-2">
  <svg><!-- ícone --></svg>
</button>

<!-- Skip links (para navegação) -->
<a href="#main-content" class="sr-only">
  Ir para conteúdo principal
</a>
```

## Validação HTML

### ✓ Inputs Corretos
```html
<!-- Email -->
<input type="email" required>

<!-- Número com step -->
<input type="number" step="0.01" min="0">

<!-- Data -->
<input type="date">

<!-- Select (não vazio) -->
<select required>
  <option value="">Selecionar...</option>
  <option value="1">Opção 1</option>
</select>

<!-- Textarea para textos longos -->
<textarea placeholder="Descrição..." rows="4"></textarea>
```

### ✗ Inputs Incorretos
```html
<!-- Type inválido -->
<input type="texto">

<!-- Sem validação -->
<input type="text" placeholder="Email">

<!-- Select vazio por padrão -->
<select>
  <option>Opção 1</option>
</select>
```

## Boas Práticas

1. **Use `<main>` para conteúdo principal**
   ```html
   <main><!-- Conteúdo único da página --></main>
   ```

2. **Use `<section>` para agrupar conteúdo relacionado**
   ```html
   <section>
     <h2>Transações Recentes</h2>
     <!-- Lista de transações -->
   </section>
   ```

3. **Use `<article>` para conteúdo independente**
   ```html
   <article><!-- Card de transação --></article>
   ```

4. **Use `<header>` e `<footer>` semanticamente**
   ```html
   <header><!-- Logo, navegação --></header>
   <footer><!-- Links, copyright --></footer>
   ```

5. **IDs só para JavaScript, Classes para CSS**
   ```html
   <!-- Classes para styling -->
   <div class="card bg-white p-4">...</div>
   
   <!-- ID para form binding ou JS -->
   <button id="btnModalAbrir">Abrir</button>
   ```

6. **Data attributes para metadados**
   ```html
   <article data-transaction-id="123" data-type="expense">
     <!-- Dados podem ser acessados via dataset em JS -->
   </article>
   ```

## Checklist

- [ ] Sem divs desnecessárias
- [ ] Tags semânticas (`<header>`, `<main>`, `<section>`, `<article>`)
- [ ] Labels associadas a inputs com `for="id"`
- [ ] Atributos `id` para JavaScript, `class` para CSS
- [ ] Alt text em imagens
- [ ] Buttons com `type` correto (submit, button, reset)
- [ ] Inputs com `type` apropriado (email, number, date)
- [ ] Links e botões distinguíveis
- [ ] Acessibilidade testada (keyboard navigation, leitores de tela)
- [ ] Estrutura que funciona sem CSS
