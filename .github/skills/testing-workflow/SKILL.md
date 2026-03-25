---
name: testing-workflow
description: 'Complete testing workflow: setup, strategy, execution, debugging. Use when: planning test coverage, setting up test suite, running tests, debugging failures, or improving test quality.'
argument-hint: 'Leave empty or specify: "setup", "strategy", "run", "debug", "coverage"'
---

# Testing Workflow - Complete Guide

Workflow completo para testes do projeto de gestão financeira. Integra com a skill `@playwright-automation` para implementação concreta.

## Princípios

1. **Teste Cedo e Frequentemente**: Testes no CI/CD a cada commit
2. **Cobertura Estratégica**: 80%+ em fluxos críticos
3. **Isolamento**: Cada teste é independente
4. **Clareza**: Testes documentam comportamento esperado
5. **Rápido**: Testes rodam em < 5 minutos
6. **Confiável**: Sem flakiness ou falsos positivos

## Quando Usar Esta Skill

1. **Setup Inicial**: Configurar suite de testes do zero
2. **Planejamento**: Definir estratégia de cobertura
3. **Execução**: Rodar testes localmente e CI/CD
4. **Debugging**: Diagnosticar falhas de teste
5. **Melhoria**: Aumentar cobertura e confiabilidade
6. **Integração**: Conectar com Playwright

## 1. SETUP - Configuração Inicial

### 1.1 Instalação

Consulte [setup guide](./assets/setup-guide.md) ou use `@playwright-automation` para:

```bash
# Instalar Playwright
npm install -D @playwright/test

# Instalar browsers
npx playwright install

# Setup estrutura de pastas
mkdir -p tests/{e2e,api,fixtures,helpers,pages,scripts}
```

### 1.2 Arquivo de Configuração

Criar `playwright.config.ts`:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 4,
  reporter: [['html'], ['json']],
  
  use: {
    baseURL: 'http://localhost:8000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
  ],

  webServer: {
    command: 'python manage.py runserver',
    url: 'http://localhost:8000',
    reuseExistingServer: !process.env.CI,
  },
});
```

### 1.3 Scripts npm

Criar em `package.json`:

```json
{
  "scripts": {
    "test": "playwright test",
    "test:watch": "playwright test --watch",
    "test:ui": "playwright test --ui",
    "test:debug": "playwright test --debug",
    "test:report": "playwright show-report",
    "test:headed": "playwright test --headed",
    "test:e2e": "playwright test tests/e2e",
    "test:api": "playwright test tests/api",
    "seed:data": "npx ts-node tests/scripts/seed-standalone.ts",
    "test:ci": "playwright test --reporter=github"
  }
}
```

## 2. STRATEGY - Planejamento de Testes

### 2.1 Matriz de Cobertura

Defina o que testar em cada camada:

| Camada | O Que Testar | Prioridade | Exemplo |
|--------|-------------|-----------|---------|
| **API** | Endpoints CRUD | 🔴 Alta | POST /api/transactions/ |
| **Autenticação** | Login/logout | 🔴 Alta | Login com email/senha |
| **Dashboard** | Visualização | 🟡 Média | Saldo visível, transações listadas |
| **Transações** | CRUD completo | 🔴 Alta | Adicionar, editar, deletar |
| **Filtros** | Funcionalidade | 🟡 Média | Filtrar por mês/categoria |
| **Mobile** | Responsividade | 🟡 Média | Touch, orientação |
| **Performance** | Carregamento | 🟢 Baixa | Dashboard < 2s |

### 2.2 Árvore de Cobertura

```
Dashboard (E2E)
├── Autenticação
│   ├── Login success
│   ├── Login failure
│   └── Logout
├── Visualização
│   ├── Saldo aparece
│   ├── Cards resumo
│   └── Transações listadas
└── Interações
    ├── Adicionar transação
    ├── Editar transação
    ├── Deletar transação
    └── Filtrar

Transações (API)
├── POST /transactions/
│   ├── Criar saída
│   ├── Criar entrada
│   ├── Validação (campos obrigatórios)
│   └── Sem autenticação (401)
├── GET /transactions/
│   ├── Listar tudo
│   ├── Filtrar mês
│   ├── Filtrar categoria
│   └── Paginação
└── PUT/DELETE /transactions/:id/
    ├── Atualizar
    ├── Deletar
    └── Permissões (403 outro usuário)
```

### 2.3 Metas de Cobertura

```
Funcionalidades Críticas:    100% (login, transações CRUD)
Funcionalidades Importantes: 80% (filtros, dashboard)
Funcionalidades Secundárias: 50% (performance, edge cases)

Total Target: 80% de cobertura de código
```

### 2.4 Tipos de Teste Recomendados

**E2E Tests (60% do tempo)**
- Fluxos completos do usuário
- Interações realistas
- Valida integração

**API Tests (30% do tempo)**
- Endpoints backend
- Validações
- Autenticação/permissões

**Component Tests (10% do tempo)**
- Componentes isolados
- Edge cases
- Sem dependências externas

## 3. EXECUTION - Executando Testes

### 3.1 Local Development

```bash
# Rodar tudo
npm test

# Modo watch (re-run ao editar)
npm run test:watch

# UI interativo
npm run test:ui

# Com browser visível
npm run test:headed

# Debug passo-a-passo
npm run test:debug

# Apenas E2E
npm run test:e2e

# Apenas API
npm run test:api
```

### 3.2 Rodar Teste Específico

```bash
# Um arquivo
npx playwright test tests/e2e/transactions.spec.ts

# Um teste específico
npx playwright test tests/e2e/transactions.spec.ts -g "adicionar saída"

# Com pattern
npx playwright test -g "transação"
```

### 3.3 Popular Dados para Teste

Use skill `@playwright-automation`:

```bash
# Via UI (com browser visível)
npm run seed:data

# Via API (mais rápido)
curl -X POST http://localhost:8000/api/transactions/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tipo":"saída","valor":85.50,"categoria":"alimentacao"}'
```

### 3.4 CI/CD Integration

Crie `.github/workflows/tests.yml`:

```yaml
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

## 4. DEBUGGING - Diagnosticando Falhas

### 4.1 Chrome DevTools

```bash
# Abrir Playwright Inspector
npm run test:debug

# Passo a passo
# - Step Over
# - Step Into
# - Continue
# - Pause
```

### 4.2 Screenshots & Videos

```typescript
// Automático em playwright.config.ts
screenshot: 'only-on-failure'  // Screenshot se falhar
video: 'retain-on-failure'     // Video se falhar

// Ver após falha
npm run test:report
```

### 4.3 Trace Viewer

```bash
# Visualizar trace completa (rede, screenshots, etc)
npx playwright show-trace trace.zip

# Em config
trace: 'on-first-retry'  // Capturar trace se falhar
```

### 4.4 Dicas de Debug

#### Teste Está Flaky?

```typescript
// 1. Verificar esperas
// ✓ Correto
await page.waitForURL('**/dashboard/**');
await page.waitForLoadState('networkidle');

// ✗ Errado
await page.waitForTimeout(2000);

// 2. Timeout aumentado
test.setTimeout(60000);

// 3. Retry automático
test.describe.configure({ retries: 2 });
```

#### Elemento Não Encontrado?

```typescript
// 1. Verificar selector
await page.pause();  // Pausar e inspecionar

// 2. Esperar elemento
await page.waitForSelector('[data-testid="add-btn"]');

// 3. Verificar visibilidade
await expect(page.locator('[data-testid="add-btn"]')).toBeVisible();

// 4. Codegen para ver selector certo
npx playwright codegen http://localhost:8000
```

#### API Test Falhando?

```typescript
// 1. Verificar resposta completa
const response = await request.post('/api/...');
console.log(response.status());
console.log(await response.json());

// 2. Verificar headers
console.log(response.headers());

// 3. Network tab (em trace)
npm run test:report
```

### 4.5 Common Issues & Fixes

| Problema | Causa | Solução |
|----------|-------|--------|
| Timeout | Elemento não aparece | `waitForLoadState('networkidle')` |
| 401 Unauthorized | Token expirado/inválido | Regenerar token em `beforeAll` |
| Flaky test | Timing inconsistente | Usar `waitForURL`, não `setTimeout` |
| Port já em uso | Servidor já rodando | `reuseExistingServer: true` |
| Screenshot preto | Page não carregou | Aguardar `loadState` |

## 5. VALIDATION - Checklist de Qualidade

### 5.1 Antes de Commit

- [ ] Todos os testes passam localmente: `npm test`
- [ ] Sem warnings ou errors
- [ ] Sem testes `.only` ou `.skip`
- [ ] Screenshots e videos não inclusos (`.gitignore`)
- [ ] Novos testes têm descrição clara

### 5.2 Antes de Deploy

- [ ] CI/CD verde (GitHub Actions)
- [ ] Cobertura ≥ 80%
- [ ] Sem testes flaky
- [ ] Relatório de testes saudável

### 5.3 Métricas de Teste

```
Total de testes: ?
├── Passando: ? (Target: 100%)
├── Falhando: 0
├── Skipped: 0
└── Tempo total: < 5 minutos

Cobertura:
├── Linhas: >= 80%
├── Branches: >= 70%
├── Functions: >= 80%
└── Statements: >= 80%
```

## 6. INTEGRATION - Usando com Playwright

### Referência Cruzada

Consulte skill `@playwright-automation` para:
- [Fixtures reutilizáveis](link-to-skill:/playwright-automation/SKILL.md)
- [E2E test examples](link-to-skill:/playwright-automation/assets/transactions.e2e.spec.ts)
- [API test examples](link-to-skill:/playwright-automation/assets/transactions.api.spec.ts)
- [Seed data helpers](link-to-skill:/playwright-automation/assets/seed-data.ts)
- [Best practices](link-to-skill:/playwright-automation/assets/best-practices.md)

### Workflow Recomendado

```
1. Definir estratégia (esta skill)
   ↓
2. Implementar testes (skill playwright-automation)
   ↓
3. Executar localmente (Esta skill - section 3)
   ↓
4. Debuggar falhas (Esta skill - section 4)
   ↓
5. CI/CD na main (Esta skill - section 3.4)
   ↓
6. Deploy com confiança ✓
```

## 7. ADVANCED - Tópicos Avançados

### Testes Parametrizados

```typescript
test.describe.configure({ retries: 2 });

import { test as base, expect } from '@playwright/test';

const transacoes = [
  { tipo: 'entrada', valor: 500 },
  { tipo: 'saída', valor: 85.50 },
  { tipo: 'entrada', valor: 1200 },
];

for (const transacao of transacoes) {
  test(`adicionar ${transacao.tipo}`, async ({ page }) => {
    // Teste parametrizado
  });
}
```

### Custom Fixtures

Veja `@playwright-automation` para exemplos.

### Teste de Performance

```typescript
test('dashboard deve carregar < 2s', async ({ page }) => {
  const start = Date.now();
  
  await page.goto('/dashboard/', { waitUntil: 'networkidle' });
  
  const duration = Date.now() - start;
  expect(duration).toBeLessThan(2000);
});
```

## Checklist Final

- [ ] Setup completo (npm, playwright.config.ts, scripts)
- [ ] Estratégia de testes definida (matriz de cobertura)
- [ ] E2E tests escrito (dashboard, transações)
- [ ] API tests escrito (CRUD endpoints)
- [ ] Fixtures reutilizáveis criadas
- [ ] CI/CD configurado (.github/workflows)
- [ ] Testes passam localmente
- [ ] CI/CD verde na branch main
- [ ] Cobertura ≥ 80%
- [ ] Documentação clara

## Recursos

- [Playwright Official](https://playwright.dev)
- [Setup Guide](./assets/setup-guide.md)
- [Testing Strategy](./assets/testing-strategy.md)
- [Debugging Guide](./assets/debugging-guide.md)
- [CI/CD Setup](./assets/ci-cd-setup.md)
- Skill: `@playwright-automation` - Implementação
