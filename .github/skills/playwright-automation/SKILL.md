---
name: playwright-automation
description: 'Playwright for E2E/component/API tests and data automation. Use when: writing tests, automating data population, testing user flows, validating UI interactions, or seeding test data.'
argument-hint: 'Leave empty or specify: "e2e", "component", "api", "seed-data", "fixtures"'
---

# Playwright Automation & Testing

Padrões completos para usar Playwright tanto para testes (E2E, Component, API) quanto para automação de dados e seed de teste.

## Princípios

1. **E2E First**: Teste fluxos reais do usuário
2. **Data Automation**: Script para popular dados rapidamente
3. **Reutilização**: Fixtures e helpers reutilizáveis
4. **Manutenibilidade**: Page objects para evitar duplicação
5. **Performance**: Testes paralelos quando possível
6. **Clareza**: Testes legíveis e autodocumentados

## Quando Usar Esta Skill

1. **E2E Tests**: Testar fluxos completos (login → adicionar transação → visualizar)
2. **Component Tests**: Testar componentes isolados
3. **API Tests**: Testar endpoints backend
4. **Seed Data**: Popular banco de dados com dados de teste
5. **Data Automation**: Automatizar preenchimento de dados via UI
6. **Fixtures**: Criar helpers para reutilizar em múltiplos testes

## Procedimento Rápido

### 1. Setup Inicial

Instale Playwright:
```bash
npm install -D @playwright/test
npx playwright install
```

Estrutura de pastas:
```
tests/
├── e2e/               # E2E tests
│   ├── auth.spec.ts
│   ├── transactions.spec.ts
│   └── dashboard.spec.ts
├── api/               # API tests
│   └── transactions.api.spec.ts
├── fixtures/          # Fixtures compartilhadas
│   ├── auth.fixture.ts
│   ├── database.fixture.ts
│   └── pages.fixture.ts
├── helpers/           # Helpers reutilizáveis
│   ├── seed-data.ts
│   ├── auth-helper.ts
│   └── transaction-helper.ts
└── playwright.config.ts
```

### 2. Fixture Básica (Autenticação)

Use [auth fixture template](./assets/auth-fixture.ts):

```typescript
// tests/fixtures/auth.fixture.ts
import { test as base } from '@playwright/test';

type AuthFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Login
    await page.goto('http://localhost:8000/login/');
    await page.fill('input[name="email"]', 'user@test.com');
    await page.fill('input[name="password"]', 'senha123');
    await page.click('button:has-text("Entrar")');
    
    // Esperar dashboard carregar
    await page.waitForURL('**/dashboard/**');
    
    await use(page);
    
    // Cleanup
    await page.close();
  },
});

export { expect } from '@playwright/test';
```

### 3. E2E Test - Adicionar Transação

```typescript
// tests/e2e/transactions.spec.ts
import { test, expect } from '../fixtures/auth.fixture';

test.describe('Adicionar Transação', () => {
  test('deve adicionar uma saída com sucesso', async ({ authenticatedPage: page }) => {
    // Arrange: Navegar até dashboard
    await page.goto('http://localhost:8000/dashboard/');
    
    // Act: Clicar em adicionar
    await page.click('button:has-text("+ Adicionar")');
    
    // Modal abre
    await expect(page.locator('#modalTransacao')).toBeVisible();
    
    // Preencher formulário
    await page.click('button:has-text("Saída")');
    await page.fill('input[name="valor"]', '85.50');
    await page.selectOption('select[name="categoria"]', 'alimentacao');
    await page.fill('input[name="data"]', '2024-03-25');
    await page.fill('input[name="descricao"]', 'Supermercado');
    
    // Salvar
    await page.click('button:has-text("Salvar")');
    
    // Assert: Verificar sucesso
    await expect(page.locator('text=Transação salva com sucesso')).toBeVisible();
    
    // Verificar se aparece na lista
    await expect(page.locator('text=Supermercado')).toBeVisible();
    
    // Verificar se saldo atualizou
    const novoSaldo = await page.locator('text=R\\$ 2.365').first();
    await expect(novoSaldo).toBeVisible();
  });
});
```

### 4. Automação de Dados (Seed Script)

Use [seed data helper](./assets/seed-data.ts):

```typescript
// tests/helpers/seed-data.ts
import { Page, Browser } from '@playwright/test';

export class SeedDataHelper {
  constructor(private page: Page) {}

  async addTransaction(data: {
    tipo: 'entrada' | 'saída';
    valor: number;
    categoria: string;
    descricao?: string;
    data?: string;
  }) {
    // Abrir modal
    await this.page.click('button:has-text("+ Adicionar")');
    await this.page.waitForSelector('#modalTransacao:not(.hidden)');

    // Selecionar tipo
    if (data.tipo === 'entrada') {
      await this.page.click('button:has-text("Entrada")');
    } else {
      await this.page.click('button:has-text("Saída")');
    }

    // Preencher campos
    await this.page.fill('input[name="valor"]', data.valor.toString());
    await this.page.selectOption('select[name="categoria"]', data.categoria);
    
    if (data.data) {
      await this.page.fill('input[name="data"]', data.data);
    }
    
    if (data.descricao) {
      await this.page.fill('input[name="descricao"]', data.descricao);
    }

    // Salvar
    await this.page.click('button:has-text("Salvar")');
    
    // Aguardar sucesso
    await this.page.waitForSelector('text=Transação salva');
    await this.page.waitForTimeout(500); // Aguardar animação
  }

  async populateTestData(count = 5) {
    const categorias = ['alimentacao', 'transporte', 'lazer', 'saude'];
    
    for (let i = 0; i < count; i++) {
      const tipo = i % 2 === 0 ? 'saída' : 'entrada';
      const valor = Math.floor(Math.random() * 1000) + 10;
      const categoria = categorias[Math.floor(Math.random() * categorias.length)];
      
      await this.addTransaction({
        tipo,
        valor,
        categoria,
        descricao: `Transação teste ${i + 1}`,
      });
    }
  }
}

export async function seedDatabase(page: Page) {
  const seedHelper = new SeedDataHelper(page);
  await seedHelper.populateTestData(10);
}
```

### 5. API Test (Backend)

```typescript
// tests/api/transactions.api.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Transactions API', () => {
  let token: string;
  const baseURL = 'http://localhost:8000/api';

  test.beforeAll(async () => {
    // Login e obter token
    const response = await fetch(`${baseURL}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'user@test.com',
        password: 'senha123',
      }),
    });
    const data = await response.json();
    token = data.token;
  });

  test('POST /transactions - criar transação', async () => {
    const response = await fetch(`${baseURL}/transactions/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        tipo: 'saída',
        valor: 85.50,
        categoria: 'alimentacao',
        descricao: 'Supermercado',
        data: '2024-03-25',
      }),
    });

    expect(response.status).toBe(201);
    const data = await response.json();
    expect(data.id).toBeDefined();
    expect(data.valor).toBe(85.50);
  });

  test('GET /transactions - listar transações', async () => {
    const response = await fetch(`${baseURL}/transactions/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    expect(response.status).toBe(200);
    const data = await response.json();
    expect(Array.isArray(data)).toBe(true);
  });
});
```

### 6. Config do Playwright

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  
  use: {
    baseURL: 'http://localhost:8000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
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

  webServer: {
    command: 'python manage.py runserver',
    url: 'http://localhost:8000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### 7. Package.json Scripts

```json
{
  "scripts": {
    "test": "playwright test",
    "test:e2e": "playwright test tests/e2e",
    "test:api": "playwright test tests/api",
    "test:debug": "playwright test --debug",
    "test:ui": "playwright test --ui",
    "test:headed": "playwright test --headed",
    "test:report": "playwright show-report",
    "seed:data": "playwright test tests/helpers/seed-data.ts --headed"
  }
}
```

## Padrões Comuns

### Page Object Pattern (Reutilizável)

```typescript
// tests/pages/DashboardPage.ts
export class DashboardPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/dashboard/');
  }

  async getSaldo(): Promise<string> {
    return this.page.locator('text=Saldo Atual')
      .locator('..').locator('text="R\\$"').first().textContent();
  }

  async openAddTransactionModal() {
    await this.page.click('button:has-text("+ Adicionar")');
    await this.page.waitForSelector('#modalTransacao:not(.hidden)');
  }

  async fillTransactionForm(data: TransactionData) {
    await this.page.fill('input[name="valor"]', data.valor.toString());
    // ... outros campos
  }

  async submitTransaction() {
    await this.page.click('button:has-text("Salvar")');
    await this.page.waitForSelector('text=salva');
  }
}
```

### Usar Page Object

```typescript
test('adicionar transação com page object', async ({ authenticatedPage: page }) => {
  const dashboard = new DashboardPage(page);
  await dashboard.goto();
  
  const saldoAntes = await dashboard.getSaldo();
  
  await dashboard.openAddTransactionModal();
  await dashboard.fillTransactionForm({
    tipo: 'saída',
    valor: 85.50,
    categoria: 'alimentacao',
  });
  await dashboard.submitTransaction();
  
  const saldoDepois = await dashboard.getSaldo();
  expect(saldoDepois).not.toBe(saldoAntes);
});
```

## Fixtures Compartilhadas

Ver [database fixture](./assets/database-fixture.ts) para:
- Setup/teardown de banco de dados
- Limpar dados entre testes
- Criar usuários de teste
- Inserir dados iniciais

## Helpers Práticos

Ver [auth helper](./assets/auth-helper.ts), [transaction helper](./assets/transaction-helper.ts):
- Login/logout
- Adicionar transações
- Filtrar transações
- Validações comuns

## Melhores Práticas

1. **Use Fixtures para Setup**
   - Não repita setup em cada teste
   - Fixtures fazem cleanup automático

2. **Page Objects para UI**
   - Locators centralizados
   - Fácil manutenção se UI mudar

3. **Dados de Teste Isolados**
   - Cada teste deve ser independente
   - Use fixtures para criar dados limpos

4. **Esperas Inteligentes**
   - Use `waitForSelector`, `waitForURL` em vez de `setTimeout`
   - Playwright espera automaticamente

5. **Relatórios**
   - Configure screenshots em falha
   - Use HTML reporter para análise

## Checklist de Implementação

- [ ] Playwright instalado e configurado
- [ ] Tests/e2e/component/api separados
- [ ] Fixtures para autenticação
- [ ] Page objects para páginas principais
- [ ] Helpers para testes repetitivos
- [ ] Seed data script funcional
- [ ] Config do Playwright
- [ ] Scripts npm para rodar testes
- [ ] CI/CD integrado
- [ ] HTML reporter configurado

## Recursos

- [Playwright Official Docs](https://playwright.dev)
- [Fixtures Documentation](https://playwright.dev/docs/test-fixtures)
- [API Testing](https://playwright.dev/docs/api-testing)
- [Debugging](https://playwright.dev/docs/debug)
- [Page Objects](https://playwright.dev/docs/test-pom)
