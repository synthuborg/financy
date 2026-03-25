# UX Checklist e Testes

Checklist completo de qualidade para garantir que a interface de gestão financeira atenda aos padrões de UX.

## Checklist Final (QA)

O sistema só está correto se TODOS os itens forem atendidos:

### 1. Clareza - Saldo Visível em 1 Segundo

- [ ] Saldo está no topo da página
- [ ] Saldo é o elemento mais destacado (maior tamanho)
- [ ] Saldo tem contraste claro contra o fundo
- [ ] Saldo é facilmente distinguível em mobile (sem scroll)
- [ ] Usuário entende o número sem qualquer contexto anterior
- [ ] Cor clara (azul primária ou destaque total)

**Teste Rápido**: Mostre a homepage para alguém por 1 segundo. Ele consegue dizer exatamente quanto é o saldo?

```html
<!-- ✓ Correto -->
<section class="bg-blue-600 p-6 text-white">
  <p class="text-sm opacity-90">Saldo Atual</p>
  <h1 class="text-5xl font-bold">R$ 2.450,50</h1>
</section>

<!-- ✗ Incorreto -->
<div class="p-2">
  <small>Seu saldo é de: R$ 2.450,50</small>
</div>
```

### 2. Rapidez - Adicionar Gasto em < 5 Segundos

- [ ] Botão "Adicionar" está sempre visível (FAB em mobile)
- [ ] Modal abre no primeiro clique
- [ ] Campo de valor tem foco automático
- [ ] Categoria tem valor padrão (ou é a primeira opção)
- [ ] Data vem preenchida com hoje
- [ ] Descrição é opcional
- [ ] Botão "Salvar" é grande e clicável
- [ ] Feedback imediato após salvar (toast/mensagem)
- [ ] Modal fecha automaticamente após salvar
- [ ] Saldo atualiza na hora

**Teste Rápido**: Cronometre um novo usuário adicionando uma despesa. Deve ser < 5 segundos.

```html
<!-- ✓ Correto -->
<!-- FAB sempre acessível -->
<button id="btnAdd" class="fixed bottom-6 right-6 w-14 h-14 bg-blue-500 rounded-full">
  +
</button>

<!-- Modal simplificado -->
<dialog id="modal">
  <input type="number" placeholder="0,00" autofocus> <!-- Foco automático -->
  <select>
    <option selected>Alimentação</option> <!-- Tem valor padrão -->
  </select>
  <input type="date" value="2024-03-25"> <!-- Data today -->
  <button type="submit">Salvar</button>
</dialog>

<!-- ✗ Incorreto -->
<!-- Botão no menu (3 cliques) -->
<nav>
  <ul>
    <li><a href="/add-transaction">Adicionar</a></li>
  </ul>
</nav>

<!-- Modal com muitos campos -->
<dialog>
  <input placeholder="Tipo..."> <!-- Sem padrão -->
  <input placeholder="Valor..."> <!-- Sem foco automático -->
  <input placeholder="Categoria..."> <!-- Buscável (lento) -->
  <input placeholder="Data...">
  <textarea placeholder="Descrição obrigatória..."></textarea> <!-- Longo -->
  <button>Salvar Transação</button> <!-- Pequeno -->
</dialog>
```

### 3. Controle - Entender Gastos Sem Esforço

- [ ] Lista de transações mostra valores com cores (vermelho/verde)
- [ ] Cada transação mostra: nome, categoria, data, valor
- [ ] Filtros por mês e categoria funcionam sem reload de página
- [ ] Query params refletem filtros (bookmarkable)
- [ ] Busca por descrição é possível
- [ ] Consegue editar/deletar transação facilmente
- [ ] Relatório simples de categorias (gráfico de barras/pizza simples)
- [ ] Histórico carregado com paginação

**Teste Rápido**: Pode um usuário saber exatamente quanto gastou com alimentação este mês em < 30 segundos?

```html
<!-- ✓ Correto -->
<!-- Valores com cores padronizadas -->
<p class="text-green-600">+R$ 3.500</p> <!-- Entrada -->
<p class="text-red-600">-R$ 85,50</p> <!-- Saída -->

<!-- Transação completa e legível -->
<article class="p-4 border rounded-lg">
  <h3 class="font-semibold">Supermercado Extra</h3>
  <p class="text-sm text-gray-600">Alimentação • Ontem 18:30</p>
  <p class="text-lg font-bold text-red-600">-R$ 85,50</p>
</article>

<!-- Filtros atualizáveis -->
<form onsubmit="aplicarFiltros(this)">
  <select name="mes">
    <option value="">Todos</option>
    <option value="03">Março</option>
  </select>
  <select name="categoria">
    <option value="">Todas</option>
    <option value="alimentacao">Alimentação</option>
  </select>
</form>

<!-- URL reflete filtros -->
<!-- URL: ?mes=03&categoria=alimentacao -->

<!-- ✗ Incorreto -->
<!-- Sem cores para entrada/saída -->
<p>+R$ 3.500 (precisa ler "entradas")</p>

<!-- Sem contexto -->
<p>Supermercado Extra - R$ 85,50</p>

<!-- Filtros exigem postback -->
<form method="POST" action="/filter">
  <!-- Recarrega página inteira -->
</form>
```

### 4. Responsividade - Mobile Perfeito

- [ ] Testado em iPhone SE (375px de largura)
- [ ] Testado em Android Google Pixel 5 (412px)
- [ ] Testado em orientação paisagem (landscape)
- [ ] Sem scroll horizontal
- [ ] Botões são clicáveis (mínimo 44px x 44px)
- [ ] Texto tem tamanho legível sem zoom
- [ ] Imagens responsivas (não overflow)
- [ ] Modal/dialogue funciona sem cortar
- [ ] Teclado virtual não esconde o conteúdo importante
- [ ] Touch targets adequados (não muito próximos)

**Teste Rápido**:
1. Abra no Google Chrome DevTools com "iPhone 12"
2. Não deve haver scroll horizontal em nenhuma página
3. Todos os botões devem ser clicáveis com dedo

```html
<!-- ✓ Correto - Mobile First -->
<!-- Começa mobile, adiciona breakpoints -->
<div class="flex flex-col gap-4 md:flex-row md:gap-6">
  <!-- Mobile: coluna, Tablet+: linha -->
</div>

<!-- FAB sempre acessível -->
<button class="fixed bottom-6 right-6 w-14 h-14">+</button>

<!-- Input com tamanho tátil -->
<input class="h-12 px-4"> <!-- 44px+ de altura -->

<!-- ✗ Incorreto - Desktop First -->
<div class="flex gap-6 md:flex-col">
  <!-- Desktop: linha (quebra em mobile!) -->
</div>

<!-- Botão pequeno -->
<button class="px-2 py-1">Ação</button>

<!-- Modal que não funciona em mobile -->
<div class="absolute left-1/4 right-1/4">
  <!-- Pode cortar em mobile -->
</div>
```

### 5. Feedback Imediato

- [ ] Spinner/loader mostra durante requisição
- [ ] Toast aparece ao salvar transação com sucesso
- [ ] Mensagem de erro clara se algo falhar
- [ ] Saldo atualiza na hora (não recarrega página)
- [ ] Filtros atualizam lista sem página recarregar
- [ ] Validação em tempo real (campo obrigatório, formato)
- [ ] Hover/focus visual claro em botões e links
- [ ] Cursor muda para pointer em elementos clicáveis

**Teste Rápido**: Adicione uma transação. Deve haver feedback visual em < 500ms.

```html
<!-- ✓ Correto -->
<!-- Loading state -->
<button id="btnSalvar" class="bg-blue-500">
  Salvar
</button>

<script>
  btnSalvar.addEventListener('click', async () => {
    btnSalvar.disabled = true;
    btnSalvar.innerHTML = 'Salvando...';
    
    await fetch('/api/transactions', { method: 'POST' });
    
    // Toast de sucesso
    mostrarToast('Transação salva!', 'success');
    
    // Atualizar saldo (sem reload)
    atualizarSaldo();
    
    // Fechar modal
    modalFechar();
  });
</script>

<!-- ✗ Incorreto -->
<!-- Sem feedback -->
<button>Salvar</button> <!-- Nada acontece visualmente -->

<!-- Página recarrega -->
<form method="POST" action="/save">
  <!-- Tela pisca, confunde usuário -->
</form>
```

### 6. Sem Fricção

- [ ] Sem campos obrigatórios desnecessários
- [ ] Sem confirmação excessiva ("Tem certeza?")
- [ ] Sem passos desnecessários
- [ ] Sem esconder funcionalidades atrás de menus
- [ ] Ações destrutivas (delete) têm confirmação SUBTILpor undo
- [ ] Sem erros criptografados
- [ ] Mensagens de erro claras (ex: "Email inválido", não "Error 400")

```html
<!-- ✓ Correto - Simples -->
<!-- Formulário com apenas 2 campos -->
<input type="number" placeholder="Valor" required>
<select required>
  <option>Alimentação</option>
</select>
<button>Salvar</button>

<!-- Ação principal sempre visível -->
<button class="fixed bottom-6 right-6">+ Adicionar</button>

<!-- ✗ Incorreto - Complicado -->
<!-- Muitos campos -->
<input placeholder="Tipo de transação?">
<input placeholder="Qual a subcategoria?">
<input placeholder="Quem você estava com?">
<input placeholder="Outro detalhe?">
<button>Próximo Passo →</button> <!-- Multi-step -->

<!-- Menu hamburger esconde tudo -->
<button>☰</button> <!-- Precisa clicar 2x pra algo -->
```

## Testes Manuais

### Teste de Clareza
```
1. Abra a página
2. Feche os olhos por 3 segundos
3. Abra e olhe por 1 segundo
4. Feche novamente
   
Pergunta: Qual é o saldo?

✓ Se respondeu corretamente = passou
```

### Teste de Velocidade
```
1. Cronometre com stopwatch
2. Clique em "+ Adicionar"
3. Digite valor
4. Selecione categoria
5. Clique em "Salvar"
6. Parar cronomômetro

✓ Se < 5 segundos = passou
✓ Se saldo atualizou na hora = passou
```

### Teste de Controle
```
1. Abra a página
2. Pergunta: Qual foi seu maior gasto este mês?
   
✓ Se respondeu em < 30 segundos = passou
✓ Se não precisou de nenhuma dica = passou
```

### Teste de Mobile
```
1. Google Chrome → DevTools → iPhone 12
2. Cada página:
   - [ ] Sem scroll horizontal
   - [ ] Botões clicável (44px+)
   - [ ] Texto legível (16px+)
   - [ ] Modal não corta
   - [ ] Topbar sticky funciona
   
✓ Se todos passaram = passou
```

### Teste de Acessibilidade
```
1. Abra a página
2. Pressione TAB múltiplas vezes
   - [ ] Focus ring sempre visível
   - [ ] Navegação sequencial lógica
   - [ ] Modais trancam focus dentro
   
3. Pressione ESC em modal
   - [ ] Modal fecha
   
4. Leia as cores (vermelho/verde)
   - [ ] Sem reliance em cor apenas
   - [ ] Ícones/texto complementam
   
✓ Se todos passaram = passou
```

## Relatório de UX

Use este template para documentar:

```markdown
## UX Report - [Data]

### Métricas Atingidas

- [ ] Saldo visível em 1 segundo
- [ ] Adicionar transação em < 5 segundos  
- [ ] Controlar gastos sem esforço
- [ ] Funciona perfeitamente no mobile
- [ ] Feedback imediato em todas as ações

### Problemas Encontrados

1. [Descrição]
   - Impacto: Alto/Médio/Baixo
   - Ação: [Corrigir]

2. [Descrição]
   - Impacto: Alto/Médio/Baixo
   - Ação: [Corrigir]

### Próximos Passos

- [ ] [Ação]
- [ ] [Ação]
```

## Checklist Final

Marque como pronto apenas quando:

- [ ] **Clareza**: Saldo entendido em 1 segundo
- [ ] **Rapidez**: Transação adicionada em < 5 segundos
- [ ] **Controle**: Hábitos entendidos sem esforço
- [ ] **Mobile**: Responsivo perfeito (sem scroll H)
- [ ] **Feedback**: Imediato em todas as ações
- [ ] **Sem fricção**: Fluxo natural e direto
- [ ] **Testado**: Chrome, Safari, Firefox, mobile (real ou DevTools)
- [ ] **Acessível**: Navegável sem mouse (TAB, ENTER, ESC)
- [ ] **Performance**: < 2s para carregar dados
- [ ] **Login**: Se necessário, < 30s do acesso ao saldo

**Quando todo checklist está completo: Pronto para produção! ✓**
