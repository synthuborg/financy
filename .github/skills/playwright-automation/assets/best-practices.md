# Playwright - Boas Práticas e Guia Completo

## Instalação e Setup

### 1. Instalar Playwright
```bash
npm install -D @playwright/test
npx playwright install
```

### 2. Estrutura de Pastas
```
tests/
├── e2e/                          # E2E (user flows)
│   ├── dashboard.spec.ts
│   ├── transactions.spec.ts
│   └── auth.spec.ts
├── api/                          # API tests
│   ├── transactions.api.spec.ts
│   └── auth.api.spec.ts
├── components/                   # Component tests
│   ├── modal.spec.ts
│   └── form.spec.ts
├── fixtures/                     # Shared fixtures
│   ├── auth.fixture.ts
│   ├── database.fixture.ts
│   └── pages.fixture.ts
├── helpers/                      # Reusable helpers
│   ├── seed-data.ts
│   ├── auth-helper.ts
│   └── transaction-helper.ts
├── pages/                        # Page objects (opcional)
│   ├── dashboard.page.ts
│   ├── login.page.ts
│   └── transaction-modal.page.ts
├── scripts/                      # Standalone scripts
│   └── seed-standalone.ts
└── playwright.config.ts          # Configuração
```

### 3. Configurar playwright.config.ts
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [['html'], ['json', { outputFile: 'test-results.json' }]],
  
  use: {
    baseURL: 'http://localhost:8000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
  ],

  webServer: {
    command: 'python manage.py runserver',
    url: 'http://localhost:8000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Selectors Melhores Práticas

### ✓ Bom (Robusto)
```typescript
// Data-testid (recomendado)
page.click('[data-testid="add-button"]');

// Has-text (user-centric)
page.click('button:has-text("Salvar")');

// Role (acessível)
page.click('button[role="primary"]');

// CSS-path (específico)
page.click('div.modal button.btn-save');
```

### ✗ Ruim (Frágil)
```typescript
// XPath complexo
page.click('//div[1]/button[3]/span[1]');

// Índices
page.click('button:nth-child(3)');

// Classe genérica
page.click('.btn');

// ID aleatório
page.click('#react-123-button');
```

### Adicionar data-testid no HTML
```html
<!-- Django template -->
<button data-testid="add-transaction-btn">
  + Adicionar
</button>

<input data-testid="transaction-value-input">
```

## Tipos de Testes

### 1. E2E Tests (User Flows)
```typescript
// Testa fluxo completo: Login → Ação → Verificação

test('usuário pode adicionar e editar transação', async ({ authenticatedPage: page }) => {
  // Arrange
  await page.goto('/dashboard/');
  
  // Act
  await page.click('[data-testid="add-transaction-btn"]');
  await page.fill('[data-testid="value-input"]', '100');
  await page.click('[data-testid="save-btn"]');
  
  // Assert
  await expect(page.locator('text=Transação salva')).toBeVisible();
});
```

### 2. Component Tests (Isolated)
```typescript
// Testa componente isoladamente (sem login necessário)

test('modal deve abrir e fechar', async ({ page }) => {
  await page.goto('/dashboard/');
  
  const modal = page.locator('#modal');
  
  // Abrir
  await page.click('[data-testid="open-modal"]');
  await expect(modal).toBeVisible();
  
  // Fechar
  await page.press('Escape');
  await expect(modal).toBeHidden();
});
```

### 3. API Tests (Backend)
```typescript
// Testa backend diretamente (sem UI)

test('POST /api/transactions deve criar', async ({ request }) => {
  const response = await request.post('/api/transactions/', {
    headers: { 'Authorization': `Bearer ${token}` },
    data: { valor: 100, categoria: 'alimentacao' },
  });

  expect(response.status()).toBe(201);
});
```

## Padrões Importantes

### 1. Fixtures (Reutilizáveis)
```typescript
// Criar fixture customizada
export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Setup
    await page.goto('/login/');
    await page.fill('input[type="email"]', 'test@test.com');
    await page.fill('input[type="password"]', 'password');
    await page.click('button:has-text("Login")');
    
    // Usar em teste
    await use(page);
    
    // Cleanup
    await page.close();
  },
});

// Usar em teste
test('com autenticação', async ({ authenticatedPage: page }) => {
  // page já está logada
  await page.goto('/dashboard/');
});
```

### 2. Page Objects (Manutenibilidade)
```typescript
// pages/TransactionModal.ts
export class TransactionModal {
  constructor(private page: Page) {}

  async open() {
    await this.page.click('[data-testid="add-btn"]');
  }

  async fillValue(value: number) {
    await this.page.fill('[data-testid="value-input"]', value.toString());
  }

  async selectCategory(category: string) {
    await this.page.selectOption('[data-testid="category-select"]', category);
  }

  async submit() {
    await this.page.click('[data-testid="save-btn"]');
  }
}

// Em teste
test('adicionar transação', async ({ page }) => {
  const modal = new TransactionModal(page);
  
  await modal.open();
  await modal.fillValue(100);
  await modal.selectCategory('alimentacao');
  await modal.submit();
  
  await expect(page.locator('text=salva')).toBeVisible();
});
```

### 3. Aguardar com Inteligência
```typescript
// ✓ Correto - Playwright aguarda automaticamente
await page.click('button');  // Aguarda elemento estar clicável
await page.fill('input', 'text');  // Aguarda elemento ser editável
await expect(page.locator('text=Sucesso')).toBeVisible();  // Aguarda aparecer

// ✗ Incorreto - Sleep cause problemas
await page.waitForTimeout(2000);  // Pode ser inconsistente
```

### 4. Dados de Teste Isolados
```typescript
// Cada teste deve ser independente
test('teste 1', async ({ cleanDatabase, page }) => {
  // Banco limpo
  // Criar dados específicos para este teste
});

test('teste 2', async ({ cleanDatabase, page }) => {
  // Banco limpo novamente
  // Dados anteriores não interferem
});
```

## Commands Úteis

```bash
# Instalar dependencies
npm install -D @playwright/test

# Rodar todos os testes
npm test

# Rodar E2E apenas
npm run test:e2e

# Rodar API apenas
npm run test:api

# Debug mode (passo a passo)
npm run test:debug

# UI mode (experimental)
npm run test:ui

# Headed (com browser visível)
npm run test:headed

# Gerar relatório
npm run test:report

# Seed de dados
npm run seed:data
```

## Debugging

### 1. Debug Mode
```bash
npx playwright test --debug
```
Em tempo real, passo a passo.

### 2. Inspect
```bash
npx playwright codegen http://localhost:8000
```
Gera código ao interagir. Ótimo para padrões.

### 3. Trace Viewer
```bash
npx playwright show-trace trace.zip
```
Replay do teste com network, screenshots, etc.

### 4. Browser DevTools
```typescript
// Pausar em ponto específico
await page.pause();
```

## Cobertura de Testes

### Checklist Básico
- [ ] E2E: Login
- [ ] E2E: Adicionar transação
- [ ] E2E: Editar transação
- [ ] E2E: Deletar transação
- [ ] E2E: Filtrar transações
- [ ] E2E: Visualizar dashboard
- [ ] API: POST transação
- [ ] API: GET transações
- [ ] API: PUT transação
- [ ] API: DELETE transação
- [ ] Mobile: Responsivo
- [ ] Mobile: Touch interactions

## Performance

### Boas Práticas
```typescript
// 1. Rodar testes em paralelo
workers: 4  // Em config

// 2. Falhar rápido
forbidOnly: true  // No CI

// 3. Retentar flaky tests
retries: 2  // Apenas no CI

// 4. Limpar entre suites
test.afterEach(async ({ page }) => {
  await page.close();
});
```

## CI/CD (GitHub Actions)

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - run: npm ci
      - run: npx playwright install --with-deps
      
      - name: Start server
        run: python manage.py runserver &
      
      - name: Run tests
        run: npm test
      
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

## Troubleshooting

### Timeout
```typescript
// Aumentar timeout globalmente
test.setTimeout(60000);

// Aumentar para action específica
await page.click('button', { timeout: 5000 });
```

### Flaky Tests
```typescript
// Retry automático
test.describe('flaky suite', () => {
  test.describe.configure({ retries: 2 });
});

// Espera mais estável
await page.waitForLoadState('networkidle');
```

### Headsless Debugging
```typescript
// Ver o que está acontecendo
const browser = await chromium.launch({ headless: false });
```

## Resources
- [Docs Oficial](https://playwright.dev)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [Debugging Guide](https://playwright.dev/docs/debug)
- [Inspector](https://playwright.dev/docs/inspector)
