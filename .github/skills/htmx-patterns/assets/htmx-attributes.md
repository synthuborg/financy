# HTMX Attributes Reference - Quick Lookup

Sintaxe completa de todos os atributos HTMX usados neste projeto.

## Request Methods

| Atributo | Uso | Exemplo |
|----------|-----|---------|
| `hx-get` | Faz GET request | `hx-get="/filter/"` |
| `hx-post` | Faz POST request | `hx-post="/create/"` |
| `hx-put` | Faz PUT request (update) | `hx-put="/edit/1/"` |
| `hx-patch` | Faz PATCH request | `hx-patch="/patch/1/"` |
| `hx-delete` | Faz DELETE request | `hx-delete="/delete/1/"` |

## Targeting & Swap

| Atributo | Uso | Exemplo |
|----------|-----|---------|
| `hx-target` | Elemento que recebe response | `hx-target="#results"` |
| `hx-target="this"` | Replace o próprio elemento | `hx-target="this"` |
| `hx-target="closest .card"` | Find ancestor com seletor | `hx-target="closest .card"` |
| `hx-target="next td"` | Find próximo elemento | `hx-target="next td"` |
| `hx-target="find .error"` | Find descendant | `hx-target="find .error"` |
| `hx-swap` | Como inserir response | `hx-swap="innerHTML"` |

### Swap Modes

| Mode | Efeito | Caso de Uso |
|------|--------|-----------|
| `innerHTML` | Replace conteúdo interno | Atualizar lista, resultados |
| `outerHTML` | Replace elemento inteiro | Deletar row, atualizar card |
| `beforebegin` | Inserir ANTES do elemento | Adicionar item no topo |
| `afterbegin` | Inserir APÓS abertura | Prepend na lista |
| `beforeend` | Inserir ANTES de fechar | Append na lista |
| `afterend` | Inserir APÓS elemento | Adicionar item depois |
| `delete` | Deletar elemento target | Remove sem conteúdo |
| `none` | Não inserir response | Só trigger eventos |

**Temporal swaps:**
```html
hx-swap="innerHTML swap:1s"  <!-- Swap after 1 second -->
hx-swap="innerHTML settle:1s" <!-- Settle/transitions after 1s -->
```

## Triggering Events

| Atributo | Uso | Exemplo |
|----------|-----|---------|
| `hx-trigger` | Quando ativar request | `hx-trigger="click"` |
| `hx-trigger="change"` | Ao mudar (selects, inputs) | `<select hx-trigger="change">` |
| `hx-trigger="submit"` | Ao enviar form | `hx-trigger="submit"` |
| `hx-trigger="keyup"` | A cada keystroke | `hx-trigger="keyup"` |
| `hx-trigger="keyup[Enter]"` | Só quando tecla específica | `hx-trigger="keyup[Enter]"` |
| `hx-trigger="every 2s"` | Polling a cada 2s | `hx-trigger="every 2s"` |
| `hx-trigger="revealed"` | Quando elemento fica visível | `hx-trigger="revealed"` |

**Modifiers:**
```html
hx-trigger="keyup delay:300ms"           <!-- Espera 300ms após última tecla -->
hx-trigger="keyup changed delay:300ms"   <!-- Só se valor mudou -->
hx-trigger="keyup from:#filter"          <!-- Triggered por outro elemento -->
```

## Data & Parameters

| Atributo | Uso | Exemplo |
|----------|-----|---------|
| `hx-vals` | Adicionar dados customizados | `hx-vals='{"category": 5}'` |
| `hx-include` | Incluir campos específicos | `hx-include="[name=*]"` |
| `hx-params` | Carregar parâmetros da URL | Automático se `hx-get="/url"` |
| `hx-replace` | Trocar parâmetros da URL | `hx-replace='{"page": "1"}'` |

**Exemplo completo:**
```html
<button hx-get="/filter/"
        hx-vals='{"category": 5, "tipo": "entrada"}'
        hx-include="[name=start_date],[name=end_date]">
  Filtrar
</button>
<!-- Envia: ?category=5&tipo=entrada&start_date=...&end_date=... -->
```

## Feedback & Indicators

| Atributo | Uso | Exemplo |
|----------|-----|---------|
| `hx-indicator` | Mostrar spinner durante request | `hx-indicator="#spinner"` |
| `hx-disabled-elt` | Desabilitar elemento | `hx-disabled-elt="this"` |
| `hx-confirm` | Confirmação antes de enviar | `hx-confirm="Confirmar?"` |
| `hx-prompt` | Prompt antes de enviar | `hx-prompt="Novo nome:"` |

**CSS classes automáticas (para indicadores):**
```css
.htmx-request {
  /* Element está em loading state */
}

.htmx-indicator {
  display: none;
}

.htmx-request .htmx-indicator {
  display: block; /* Mostrar durante request */
}

.htmx-indicator.htmx-settling {
  /* After response, settling period */
}
```

## Response Headers

Server pode responder com headers HTMX:

```python
# Django view
def my_view(request):
    # ...
    response = render(request, 'template.html', context)
    response['HX-Redirect'] = '/dashboard/'  # Redirecionar
    response['HX-Refresh'] = 'true'           # Recarregar página
    response['HX-Push-Url'] = '/new-url/'    # Atualizar URL no navegador
    response['HX-Trigger'] = 'dataUpdated'    # Trigger evento customizado
    return response
```

## Advanced: Events & Lifecycle

```html
<!-- Trigger HTMX lifecycle events -->
<div hx-get="/data/">
  <!-- Eventos disponíveis: -->
  htmx:xhr:loadstart
  htmx:xhr:loadprogress
  htmx:xhr:abort
  htmx:responseError
  htmx:sendError
  htmx:timeout
  htmx:beforeRequest
  htmx:afterRequest
  htmx:beforeSwap
  htmx:afterSwap
  htmx:settlingStart
  htmx:settlingEnd
</div>

<!-- Escutar eventos -->
<script>
  document.body.addEventListener('htmx:afterSwap', function(detail) {
    console.log('Conteúdo foi trocado');
  });
</script>
```

## Cheatsheet: Common Patterns

### Filter Buttons

```html
<button hx-get="/filter/" 
        hx-vals='{"category": 5}' 
        hx-target="#list"
        hx-swap="innerHTML">
  Categoria
</button>
```

### Live Search

```html
<input type="text" 
       name="q"
       hx-get="/search/" 
       hx-trigger="keyup changed delay:300ms"
       hx-target="#results">
```

### Pagination Links

```html
<a hx-get="/items/" 
   hx-vals='{"page": 2}' 
   hx-target="#items-list"
   hx-swap="innerHTML">
  Próxima
</a>
```

### Delete with Confirmation

```html
<button hx-delete="/delete/123/" 
        hx-confirm="Deletar?"
        hx-target="closest tr"
        hx-swap="outerHTML">
  Deletar
</button>
```

### Form Submit

```html
<form hx-post="/create/" 
      hx-target="#response"
      hx-swap="innerHTML">
  <!-- fields... -->
  <button type="submit">Criar</button>
</form>
```

### Polling

```html
<div hx-get="/status/" 
     hx-trigger="every 5s"
     hx-swap="innerHTML">
  Status: Loading...
</div>
```

### Infinite Scroll

```html
<div id="items">
  <!-- items... -->
</div>

<div hx-get="/items/?page=2"
     hx-trigger="revealed"
     hx-swap="beforeend"
     hx-target="#items">
  Load more...
</div>
```

## Response Partial Example

View should return only the swap portion:

```html
<!-- ✅ Certo: Apenas items (sem body/html) -->
<div class="item">Item 1</div>
<div class="item">Item 2</div>

<!-- ✗ Errado: Página completa -->
<!DOCTYPE html>
<html>
  <body>...</body>
</html>
```

## URL Query Strings Built Automatically

HTMX monta query strings automaticamente:

```html
<!-- Input com name="q" -->
<input hx-get="/search/" name="q">
<!-- Envia: GET /search/?q=user-typed-text -->

<!-- Múltiplos campos -->
<input hx-get="/filter/" name="start_date">
<input hx-get="/filter/" name="end_date">
<!-- Envia: GET /filter/?start_date=2024-01-15&end_date=2024-01-20 -->

<!-- Customizar com hx-vals -->
<button hx-get="/filter/" hx-vals='{"category": 5}' name="page">
<!-- Envia: GET /filter/?category=5&page=1 (if form filled) -->
```

## Debugging Attributes

```html
<!-- Ver requisições HTMX no console -->
<script>
  htmx.logAll();
</script>

<!-- Ou inspecionar elemento -->
<button hx-get="/test/" hx-target="#result" hx-swap="innerHTML">
  Test
</button>

<!-- DevTools:
  1. Abra Network tab
  2. Clique button
  3. Veja request em /test/
  4. Response deve ser HTML parcial
-->
```

## Compatibilidade

```html
<!-- HTMX requer: -->
- HTTP/1.1 ou HTTP/2
- JavaScript habilitado
- XMLHttpRequest ou Fetch API

<!-- Fallback para sem JS: -->
<!-- Use <a href="/old-url/"> ou <form method="post"> -->
```

---

**Ver exemplos práticos:** [Component Examples](component-examples.md)  
**Ver implementação Django:** [Django Views HTMX](django-views-htmx.md)
