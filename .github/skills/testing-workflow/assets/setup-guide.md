# Setup Guide - Configuração Completa

Passo-a-passo para setupar Playwright e testes do zero.

## Pré-requisitos

- Node.js 18+
- Python 3.9+
- Django rodando em localhost:8000

## Instalação Rápida

### 1. Instalar Playwright

```bash
npm install -D @playwright/test
npx playwright install
```

### 2. Criar Estrutura

```bash
mkdir -p tests/{e2e,api,fixtures,helpers,pages,scripts}
```

### 3. Copiar Configuração

Crie `playwright.config.ts`:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 4,
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results.json' }],
    ['junit', { outputFile: 'junit.xml' }],
  ],
  
  use: {
    baseURL: 'http://localhost:8000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],

  globalSetup: './tests/setup.ts',
  globalTeardown: './tests/teardown.ts',

  webServer: {
    command: 'python manage.py runserver',
    url: 'http://localhost:8000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

### 4. Configurar package.json

```json
{
  "name": "hackaton-financas-tests",
  "version": "1.0.0",
  "scripts": {
    "test": "playwright test",
    "test:watch": "playwright test --watch",
    "test:ui": "playwright test --ui",
    "test:debug": "playwright test --debug",
    "test:report": "playwright show-report",
    "test:headed": "playwright test --headed",
    "test:e2e": "playwright test tests/e2e",
    "test:api": "playwright test tests/api",
    "test:ci": "playwright test --reporter=github",
    "seed:data": "npx ts-node tests/scripts/seed-standalone.ts",
    "codegen": "playwright codegen http://localhost:8000"
  },
  "devDependencies": {
    "@playwright/test": "^1.40.0",
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0"
  }
}
```

### 5. Setup/Teardown Global

Crie `tests/setup.ts`:

```typescript
import { chromium } from '@playwright/test';

async function globalSetup() {
  console.log('🔧 Setup global...');
  
  // Opcionalmente: criar dados de teste
  // Opcionalmente: resetar banco
  
  console.log('✅ Setup completo!');
}

export default globalSetup;
```

Crie `tests/teardown.ts`:

```typescript
async function globalTeardown() {
  console.log('🧹 Limpando dados de teste...');
  // Opcionalmente: deletar dados de teste criados
  console.log('✅ Cleanup completo!');
}

export default globalTeardown;
```

### 6. Primeiros Testes

Use modelos da skill `@playwright-automation`:
- [auth-fixture.ts](link-to-skill:/playwright-automation/assets/auth-fixture.ts)
- [transactions.e2e.spec.ts](link-to-skill:/playwright-automation/assets/transactions.e2e.spec.ts)

Copie e adapte para seu projeto.

### 7. Rodar Primeiro Teste

```bash
npm test
```

Deve aparecer:
```
✓ tests/e2e/... (XXms)
✓ tests/api/... (XXms)

XX passed
```

## Troubleshooting Setup

### Porta 8000 já em uso

```bash
# Encontrar processo
lsof -i :8000

# Matar processo
kill -9 <PID>
```

### Playwright browsers não instalados

```bash
npx playwright install
npx playwright install-deps
```

### TypeScript não compilando

```bash
npm install -D ts-node typescript @types/node
npx tsc --init
```

### Django não conecta

```bash
# Verificar se Django está rodando
python manage.py runserver

# Em outro terminal
npm test
```

## Verificação Final

```bash
✓ Node.js 18+
✓ npm install -D @playwright/test
✓ npx playwright install
✓ playwright.config.ts existe
✓ package.json tem scripts
✓ tests/ folder criada
✓ Primeiro teste passa
✓ Django rodando em 8000
✓ npm test funciona

Pronto! 🚀
```
