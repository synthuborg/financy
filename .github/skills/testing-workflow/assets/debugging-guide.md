# Debugging Guide - Resolvendo Problemas

Guia prático para debugar e resolver falhas em testes.

## Modo Debug Interativo

### 1. Debugar com DevTools Integrado

```bash
# Abre Chrome DevTools durante o teste
npx playwright test --debug

# Ou com UI mode
npx playwright test --ui
```

Controles:
- `Step over` (F10) - próxima linha
- `Step into` (F11) - entra em função
- `Continue` (F5) - até próximo breakpoint
- `Watch expressions` - inspecionar variáveis

### 2. Usar page.pause()

```typescript
test('debugar especificamente', async ({ page }) => {
  await page.goto('/dashboard');
  await page.pause(); // ⏸️ Pausa aqui, abre DevTools
  
  // Continue explorando manualmente
});
```

### 3. Ativar Verbose Logging

```bash
npx playwright test --debug
# Amostra em browser:
# → navigating to http://localhost:8000/dashboard
# ← navigation to url succeeded
# → clicking on button
# ← click action finished

# Ou via código
test.describe.configure({ mode: 'parallel' });
const debug = true;
```

## Screenshots & Videos

### Capturar Screenshots

```typescript
test('screenshot em falha', async ({ page }) => {
  await page.goto('/transactions');
  
  // Sempre capturar
  await page.screenshot({ path: 'full-page.png', fullPage: true });
  
  // Só em falha (auto)
  await page.screenshot({ path: 'error.png' });
});
```

Ver screenshot:
```bash
npx playwright show-report
```

### Gravar Vídeo

Config automática em `playwright.config.ts`:

```typescript
use: {
  video: 'retain-on-failure', // grava só se falhar
  // Opções: 'off', 'on', 'retain-on-failure'
},

// Via código
test('com vídeo', async ({ page }) => {
  // vídeo grava automaticamente
});
```

Ver vídeo:
```bash
npx playwright show-report
# Clique em test → video player
```

## Trace Viewer

### Ativar Trace

```typescript
use: {
  trace: 'on-first-retry',
  // Opções: 'off', 'on', 'retain-on-failure', 'on-first-retry'
},
```

### Abrir Trace

```bash
npx playwright show-trace test-results/trace.zip
```

**Trace mostra:**
- Todos os eventos do DOM
- Screenshots progressivos
- Network requests
- Console logs
- Async calls

## Problemas Comuns & Soluções

### ❌ Timeout: element not found

```
Error: Timeout 30000ms exceeded. waitForSelector failed: selector resolved to hidden <input>
```

**Causa:** Elemento não existe ou está hidden.

**Solução:**

```typescript
// ❌ Errado: espera elemento existir
await page.click('button[data-test="submit"]');

// ✅ Certo: verifica antes
const button = page.locator('button[data-test="submit"]');
await button.waitFor({ state: 'visible' });
await button.click();

// Ou com timeout customizado
await page.locator('button').first().click({ timeout: 5000 });
```

**Debug:**

```typescript
// Ver o que existe
const html = await page.content();
console.log(html);

// Ou tirar screenshot
await page.screenshot({ path: 'debug.png' });

// Abrir em DevTools
await page.pause();
```

### ❌ Timeout: element not enabled

```
Error: element is not enabled
```

**Causa:** Button desabilitado, input readonly, etc.

**Solução:**

```typescript
// ❌ Errado
await page.click('button[type="submit"]');

// ✅ Certo: esperar estar habilitado
await page.locator('button[type="submit"]').isEnabled();
await page.click('button[type="submit"]');

// Ou debugar
test('verificar estado', async ({ page }) => {
  const button = page.locator('button.submit');
  
  // Checklist
  console.log(await button.isVisible()); // true?
  console.log(await button.isEnabled()); // true?
  console.log(await button.getAttribute('disabled')); // null?
  
  if (!await button.isEnabled()) {
    await page.pause(); // inspecione por quê
  }
});
```

### ❌ Flaky Test: Sometimes Passes, Sometimes Fails

```
✓ Test passed on attempt 1
✗ Test failed on attempt 2
```

**Causa:** Timing aleatório, race condition, async não esperado.

**Solução:**

```typescript
// ❌ Errado: não espera
await page.goto('/dashboard');
const text = await page.locator('text=Saldo: 100').textContent();

// ✅ Certo: espera elemento estar ready
await page.goto('/dashboard');
await page.locator('text=Saldo: 100').waitFor();
const text = await page.locator('text=Saldo: 100').textContent();

// Ou esperar rede
await page.goto('/dashboard', { waitUntil: 'networkidle' });

// Ou API call específico
await page.waitForResponse(response =>
  response.url().includes('/api/saldo/') && response.status() === 200
);
```

### ❌ Assertion Error: text not found

```
Error: expect(received).toContain(expected)
Expected: "Saldo: 100.00"
Actual:   "Saldo100.00"
```

**Causa:** Whitespace, formatação de número.

**Solução:**

```typescript
// ❌ Errado: muito específico
expect(await page.locator('text=Saldo: 100.00').textContent())
  .toBe('Saldo: 100.00');

// ✅ Certo: normalizar
expect(await page.locator('.saldo').textContent())
  .toMatch(/Saldo:\s*100\.00/);

// Ou getByText com regex
await page.getByText(/Saldo.*100/).click();
```

### ❌ "Page closed or redirected"

```
Error: Target page, context or browser has been closed or is no longer available
```

**Causa:** Page fecha inesperadamente, navegação.

**Solução:**

```typescript
// ❌ Errado: assume página permanece aberta
await page.goto('/logout');
await page.click('button');  // página pode fechar

// ✅ Certo: criar nova page se necessário
await page.goto('/logout');
await page.context().newPage(); // nova page se precisar
```

### ❌ Network Error: Connection refused

```
Error: net::ERR_CONNECTION_REFUSED
```

**Causa:** Django não rodando na porta 8000.

**Solução:**

```bash
# Verificar Django
python manage.py runserver 0.0.0.0:8000

# Ou em teste
test.beforeAll(async () => {
  // Esperar Django estar ready
  const response = await fetch('http://localhost:8000/');
  if (!response.ok) {
    throw new Error('Django não conecta em 8000');
  }
});
```

### ❌ Auth Fails: 401 Unauthorized

```
Error: Response status 401
```

**Causa:** Token expirado, fixture auth não funcion.

**Solução:**

```typescript
// Usar fixture corretamente
import { authenticatedPage } from './fixtures/auth-fixture';

test('usa fixture auth', async ({ authenticatedPage, request }) => {
  const response = await request.get('/api/transactions/', {
    headers: {
      'Authorization': `Bearer ${await getToken()}` // token do storage
    }
  });
  expect(response.status()).toBe(200);
});

// Ou debugar manualmente
test('verificar token', async ({ page }) => {
  await page.goto('/login');
  
  // Preencher credenciais
  await page.fill('input[name="username"]', 'testuser');
  await page.fill('input[name="password"]', 'testpass');
  await page.click('button[type="submit"]');
  
  // Verificar token foi salvo
  await page.pause(); // abrir DevTools
  // localStorage → está token?
  
  const token = await page.evaluate(() => localStorage.getItem('token'));
  console.log('Token:', token);
});
```

### ❌ CORS Error

```
Error: Access to XMLHttpRequest blocked by CORS
```

**Causa:** Django não permite origem do teste.

**Solução:**

```python
# settings.py Django
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Ou aceitar qualquer (desenvolvimento apenas!)
CORS_ALLOW_ALL_ORIGINS = True
```

## Inspector & Codegen

### Registrar Ações Automaticamente

```bash
npx playwright codegen http://localhost:8000
```

**Abre:**
- Browser normal
- Action recorder
- Code gerador lado a lado

**Usar:**
1. Clique, type, select no browser
2. Code apareça automaticamente
3. Copy para teste

### Inspector Tool

```bash
# Usar seletores interativamente
npx playwright test --inspector

# Ou com debug
npx playwright test --debug --inspector
```

**Funções:**
- Test explorer
- Locator picker (clique em elemento)
- Verify seletor
- Copy código

## Performance Debugging

### Medir Tempo de Operação

```typescript
test('medir performance', async ({ page }) => {
  const start = Date.now();
  
  await page.goto('/dashboard');
  const loadTime = Date.now() - start;
  
  expect(loadTime).toBeLessThan(1000); // 1s
  console.log(`Dashboard carregou em ${loadTime}ms`);
});
```

### Network Watchers

```typescript
test('monitorar requisições', async ({ page }) => {
  // Log todas requisições
  page.on('request', request => {
    console.log(`→ ${request.method()} ${request.url()}`);
  });
  
  page.on('response', response => {
    console.log(`← ${response.status()} ${response.url()}`);
  });
  
  // Coletar tempo de resposta
  page.on('response', response => {
    if (response.url().includes('/api/')) {
      const timing = response.timing();
      console.log(`API respondeu em ${timing.responseEnd}ms`);
    }
  });
  
  await page.goto('/dashboard');
});
```

## CI Debugging

### Local CI Simulation

```bash
# Simular ambiente CI (single worker, retries)
npm run test:ci

# Ou manualmente
npx playwright test --workers=1 --retries=2
```

### GitHub Actions Logs

1. Ir a Actions → test workflow → falha
2. Ver logs completos
3. Buscar por "Error:"

```yaml
# .github/workflows/test.yml - com debug
- name: Run tests with debug
  run: npx playwright test
  env:
    DEBUG: pw:api
```

## Checklist de Debugging

- [ ] Teste passa em UI mode (`--ui`)?
- [ ] Mesmo resultado em headed (`--headed`) vs headless?
- [ ] Funciona em Chrome, Firefox, Safari?
- [ ] Timeout adequado (default 30s)?
- [ ] Esperas explícitas antes de assertions?
- [ ] Screenshot em falha está claro?
- [ ] Vídeo mostra o problema?
- [ ] Trace mostra sequência correta?
- [ ] Seletor é único/determinístico?
- [ ] Não depende de timing?
- [ ] Auth fixture funcionando?
- [ ] Django rodando?
- [ ] Rede/CORS OK?

## Dicas Profissionais

### 1. Use Data Attributes para Seletores

```html
<!-- Good 👍 -->
<button data-test="submit">Submit</button>

<!-- Bad 👎 -->
<button class="btn btn-primary">Submit</button>
```

```typescript
// Usar no teste
await page.click('[data-test="submit"]');
```

### 2. Esperar Elementos com Wait

```typescript
// ❌ Rápido demais
await page.fill('input[name="email"]', 'test@test.com');

// ✅ Com espera
await page.waitForSelector('input[name="email"]');
await page.fill('input[name="email"]', 'test@test.com');
```

### 3. Usar Page Object Model

```typescript
// pages/TransactionPage.ts
export class TransactionPage {
  constructor(private page: Page) {}
  
  async goto() {
    await this.page.goto('/transactions');
  }
  
  async fillForm(data: Transaction) {
    await this.page.fill('input[name="valor"]', data.valor);
    await this.page.fill('input[name="descricao"]', data.descricao);
  }
  
  async submit() {
    await this.page.click('button[type="submit"]');
  }
}
```

### 4. Reuse Data de Teste

```typescript
// Seedar uma vez
test.beforeAll(async () => {
  await seedTestData();
});

// Usar em múltiplos testes
test('test 1', async ({ page }) => { /*...*/ });
test('test 2', async ({ page }) => { /*...*/ });
```

## Próximos Passos

1. [Setup Inicial](setup-guide.md)
2. [Estratégia de Testes](testing-strategy.md)
3. [CI/CD Integration](ci-cd-setup.md)
4. Usar [Playwright Automation Skills](link-to-skill:/playwright-automation)
