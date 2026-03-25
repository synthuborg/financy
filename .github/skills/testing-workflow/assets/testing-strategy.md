# Testing Strategy - Estratégia de Testes Completa

Matriz e planejamento detalhado de testes para hackaton_app_financas.

## Matriz de Cobertura

### Tier 1: Crítico (Deve ter 100% cobertura)

```
📊 Dashboard
├─ ✅ Saldo carrega em < 1s
├─ ✅ Transações filtram por período
├─ ✅ Categorias filtram corretamente
├─ ✅ Gráficos renderizam
└─ ✅ Mobile display correto

💰 Transações
├─ ✅ Criar entrada
├─ ✅ Criar saída
├─ ✅ Editar transação
├─ ✅ Deletar transação
├─ ✅ Validação de campo obrigatório
├─ ✅ Validação de valor
└─ ✅ Validação de data

🔐 Autenticação
├─ ✅ Login com credenciais corretas
├─ ✅ Rejeita credenciais inválidas
├─ ✅ Logout limpa session
├─ ✅ Sem token → redirect /login
└─ ✅ Token expirado → re-login
```

### Tier 2: Importante (80%+ cobertura esperada)

```
📈 Relatórios
├─ ✅ Resumo mensal calcula corretamente
├─ ✅ Resumo por categoria
├─ ✅ Export CSV funciona
├─ ✅ Export PDF renderiza
└─ ✅ Comparação mês anterior

🏷️ Categorias
├─ ✅ Listar categorias
├─ ✅ Criar categoria
├─ ✅ Editar categoria
├─ ✅ Deletar categoria
└─ ✅ Permissão por usuário

👤 Perfil
├─ ✅ Editar perfil
├─ ✅ Alterar senha
├─ ✅ Atualizar avatar
└─ ✅ Preferências salvas
```

### Tier 3: Adicional (50%+ cobertura)

```
🔔 Notificações
├─ ✅ Email confirmação cadastro
├─ ✅ Alert limite superado
├─ ✅ Lembrete pagamento
└─ ✅ Relatório semanal

🌐 Integração
├─ ✅ Multi-dispositivo sincroniza
├─ ✅ Offline mode básico
└─ ✅ Exportar dados
```

## Matriz de Prioridade

```
┌─────────────────────┬──────────┬──────────────┐
│ Feature             │ Priority │ Effort (hrs) │
├─────────────────────┼──────────┼──────────────┤
│ Dashboard           │ 🔴 P0    │ 4            │
│ Add Transaction     │ 🔴 P0    │ 3            │
│ Edit/Delete Trans   │ 🟠 P1    │ 2            │
│ Filtros             │ 🟠 P1    │ 2            │
│ Relatórios          │ 🟠 P1    │ 4            │
│ Categorias          │ 🟡 P2    │ 2            │
│ Perfil              │ 🟡 P2    │ 2            │
│ Notificações        │ 🟢 P3    │ 3            │
│ Export              │ 🟢 P3    │ 2            │
├─────────────────────┼──────────┼──────────────┤
│ TOTAL               │          │ 24 hrs       │
└─────────────────────┴──────────┴──────────────┘
```

## Test Types Coverage

### E2E Tests (40% do tempo)

**Objetivo:** Testar fluxo completo do usuário

```typescript
// 1. User Journey: Criar transação
- Login
- Navegar para nova transação
- Preencher form
- Validar salvo
- Ver no dashboard

// 2. User Journey: Adicionar categoria
- Login
- Settings → Categorias
- Novo
- Preencher
- Usar em transação

// 3. User Journey: Ver relatório
- Login
- Dashboard
- Click "Relatório"
- Filtrar período
- Export PDF
```

**Exemplos:** [transactions.e2e.spec.ts](link-to-skill:/playwright-automation/assets/transactions.e2e.spec.ts)

### API Tests (30% do tempo)

**Objetivo:** Testar lógica sem UI

```typescript
// 1. POST /transactions/
- Validação (campos obrigatórios)
- Cálculo saldo
- Auditoria

// 2. GET /transactions/
- Paginação
- Filtro por categoria
- Filtro por período
- Sort

// 3. PUT /transactions/{id}/
- Atualizar
- Validação
- Permissão

// 4. DELETE /transactions/{id}/
- Deletar
- Auditoria
- Não retorna mais
```

**Exemplos:** [transactions.api.spec.ts](link-to-skill:/playwright-automation/assets/transactions.api.spec.ts)

### Component Tests (20% do tempo)

**Objetivo:** Testar componentes isolados

```typescript
// 1. TransactionForm
- Renderiza campos corretos
- Validação inline
- Submit ativa button

// 2. SaldoCard
- Formata valor
- Cor verde/vermelha
- Atualiza ao mudar data

// 3. TransactionList
- Renderiza items
- Paginação funciona
- Ordenação
```

### Performance Tests (10% do tempo)

**Objetivo:** Testar velocidade crítica

```typescript
// 1. Dashboard Load Time
- First contentful paint < 1s
- Saldo < 500ms
- Transactions < 2s

// 2. Search Performance
- 1000 transações
- Busca < 500ms
- Filtro < 300ms

// 3. Mobile Performance
- Em 3G
- Saldo ainda < 2s
- Interativo em < 3s
```

## Checklist de Planejamento

### Antes de Começar

- [ ] Definir escopo de features
- [ ] Priorizar por valor para usuário
- [ ] Estimar esforço
- [ ] Alocar tempo por tier
- [ ] Setup ambiente de teste

### Durante Desenvolvimento

- [ ] Escrever testes ANTES de código (TDD)
- [ ] Rodar testes antes de commit
- [ ] Manter > 80% coverage crítico
- [ ] Revisão de testes em PR
- [ ] Atualizar matriz quando feature muda

### Antes de Deploy

- [ ] Todos Tier 1 passando
- [ ] Todos Tier 2 em 80%+
- [ ] Sem erros no CI
- [ ] Coverage report OK
- [ ] Performance base line OK

## Exemplo: Testando "Criar Transação"

### E2E Test (user perspective)

```typescript
test('criar transação de entrada', async ({ page, authenticatedPage }) => {
  await page.goto('/transactions/new');
  
  await page.fill('input[name="valor"]', '100.00');
  await page.selectOption('select[name="categoria"]', 'salario');
  await page.fill('input[name="descricao"]', 'Salário');
  await page.fill('input[name="data"]', '2024-01-15');
  
  await page.click('button[type="submit"]');
  await page.waitForURL('/transactions');
  
  // Verificar no dashboard
  expect(page.locator('text=Salário')).toBeVisible();
  expect(page.locator('text=+100.00')).toBeVisible();
});
```

### API Test (backend perspective)

```typescript
test('POST /transactions/ com validação', async ({ request }) => {
  const response = await request.post('/api/transactions/', {
    data: {
      tipo: 'entrada',
      valor: 100.00,
      categoria_id: 1,
      descricao: 'Salário',
      data: '2024-01-15'
    }
  });
  
  expect(response.status()).toBe(201);
  const json = await response.json();
  expect(json.id).toBeDefined();
  expect(json.saldo_atualizado).toBe(true);
});
```

### Component Test (field level)

```typescript
test('validação em tempo real', async ({ page }) => {
  await page.goto('/transactions/new');
  
  // Campo vazio
  await page.fill('input[name="valor"]', '');
  await page.click('input[name="descricao"]');
  expect(page.locator('text=Campo obrigatório')).toBeVisible();
  
  // Valor inválido
  await page.fill('input[name="valor"]', 'abc');
  await page.click('input[name="descricao"]');
  expect(page.locator('text=Valor inválido')).toBeVisible();
  
  // Válido
  await page.fill('input[name="valor"]', '100.00');
  expect(page.locator('text=Campo obrigatório')).not.toBeVisible();
});
```

## Integração com @playwright-automation

Use fixtures e helpers da skill Playwright:

```typescript
// auth-fixture.ts
import { authenticatedPage } from './fixtures/auth-fixture';

test('usa fixture autenticado', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/dashboard');
});
```

```typescript
// seed-data.ts
import { SeedDataHelper } from './helpers/seed-data';

test('com dados seedados', async ({ page }) => {
  const seeder = new SeedDataHelper(page);
  
  // Popula 10 transações automaticamente
  await seeder.populateTestData(10);
  
  await page.goto('/dashboard');
  expect(page.locator('text=10 transações')).toBeVisible();
});
```

## Métricas de Sucesso

```
Cobertura:
- Tier 1: 100%
- Tier 2: 80%+
- Tier 3: 50%+
- Overall: 75%+

Performance:
- Dashboard: < 1s
- Transações: < 2s
- Search: < 500ms

Confiabilidade:
- Flakiness: < 1%
- Retry rate: < 5%
- Success rate: > 99%
```

## Próximos Passos

1. [Setup Environment](setup-guide.md)
2. [Run Tests Locally](ci-cd-setup.md#local)
3. [Debug Failures](debugging-guide.md)
4. [CI/CD Integration](ci-cd-setup.md)
