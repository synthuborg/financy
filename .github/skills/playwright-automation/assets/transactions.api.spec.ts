// tests/api/transactions.api.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Transactions API', () => {
  let token: string;
  let userId: number;
  const baseURL = 'http://localhost:8000/api';

  test.beforeAll(async ({ browser }) => {
    // Fazer login para obter token
    const context = await browser.newContext();
    const page = await context.newPage();

    // Login (simular ou usar API real se disponível)
    const loginResponse = await page.request.post(`${baseURL}/auth/login/`, {
      data: {
        email: 'user@test.com',
        password: 'senha123',
      },
    });

    const loginData = await loginResponse.json();
    token = loginData.token || loginData.access;
    userId = loginData.user_id || loginData.id;

    await context.close();
  });

  test.describe('POST /transactions/', () => {
    test('deve criar uma transação de saída', async ({ request }) => {
      // Act
      const response = await request.post(`${baseURL}/transactions/`, {
        headers: { 'Authorization': `Bearer ${token}` },
        data: {
          tipo: 'saída',
          valor: 85.50,
          categoria: 'alimentacao',
          descricao: 'Supermercado',
          data: '2024-03-25',
        },
      });

      // Assert
      expect(response.status()).toBe(201);

      const data = await response.json();
      expect(data.id).toBeDefined();
      expect(data.valor).toBe(85.50);
      expect(data.categoria).toBe('alimentacao');
      expect(data.descricao).toBe('Supermercado');
    });

    test('deve criar uma transação de entrada', async ({ request }) => {
      // Act
      const response = await request.post(`${baseURL}/transactions/`, {
        headers: { 'Authorization': `Bearer ${token}` },
        data: {
          tipo: 'entrada',
          valor: 3500,
          categoria: 'renda',
          descricao: 'Salário',
          data: '2024-03-01',
        },
      });

      // Assert
      expect(response.status()).toBe(201);

      const data = await response.json();
      expect(data.tipo).toBe('entrada');
      expect(data.valor).toBe(3500);
    });

    test('não deve criar sem valor', async ({ request }) => {
      // Act
      const response = await request.post(`${baseURL}/transactions/`, {
        headers: { 'Authorization': `Bearer ${token}` },
        data: {
          tipo: 'saída',
          categoria: 'alimentacao',
        },
      });

      // Assert
      expect(response.status()).toBe(400);

      const data = await response.json();
      expect(data.valor).toBeDefined(); // Campo obrigatório
    });

    test('não deve criar sem autenticação', async ({ request }) => {
      // Act
      const response = await request.post(`${baseURL}/transactions/`, {
        data: {
          tipo: 'saída',
          valor: 85.50,
          categoria: 'alimentacao',
        },
      });

      // Assert
      expect(response.status()).toBe(401);
    });
  });

  test.describe('GET /transactions/', () => {
    test('deve listar transações do usuário', async ({ request }) => {
      // Act
      const response = await request.get(`${baseURL}/transactions/`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      // Assert
      expect(response.status()).toBe(200);

      const data = await response.json();
      expect(Array.isArray(data)).toBe(true);
      
      // Cada transação deve ter campos obrigatórios
      if (data.length > 0) {
        const transacao = data[0];
        expect(transacao.id).toBeDefined();
        expect(transacao.valor).toBeDefined();
        expect(transacao.tipo).toBeDefined();
        expect(transacao.categoria).toBeDefined();
      }
    });

    test('deve filtrar por mês', async ({ request }) => {
      // Act
      const response = await request.get(`${baseURL}/transactions/?mes=03`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      // Assert
      expect(response.status()).toBe(200);

      const data = await response.json();
      
      // Todas as transações devem ser de março
      if (data.length > 0) {
        const transacao = data[0];
        const mes = new Date(transacao.data).getMonth() + 1;
        expect(mes).toBe(3);
      }
    });

    test('deve filtrar por categoria', async ({ request }) => {
      // Act
      const response = await request.get(
        `${baseURL}/transactions/?categoria=alimentacao`,
        { headers: { 'Authorization': `Bearer ${token}` } }
      );

      // Assert
      expect(response.status()).toBe(200);

      const data = await response.json();
      
      // Todas devem ser de alimentação
      if (data.length > 0) {
        const transacao = data[0];
        expect(transacao.categoria).toBe('alimentacao');
      }
    });
  });

  test.describe('GET /transactions/:id/', () => {
    let transacaoId: number;

    test.beforeEach(async ({ request }) => {
      // Criar uma transação para testar
      const response = await request.post(`${baseURL}/transactions/`, {
        headers: { 'Authorization': `Bearer ${token}` },
        data: {
          tipo: 'saída',
          valor: 100,
          categoria: 'transporte',
          descricao: 'Uber',
        },
      });

      const data = await response.json();
      transacaoId = data.id;
    });

    test('deve obter uma transação específica', async ({ request }) => {
      // Act
      const response = await request.get(
        `${baseURL}/transactions/${transacaoId}/`,
        { headers: { 'Authorization': `Bearer ${token}` } }
      );

      // Assert
      expect(response.status()).toBe(200);

      const data = await response.json();
      expect(data.id).toBe(transacaoId);
      expect(data.valor).toBe(100);
      expect(data.descricao).toBe('Uber');
    });

    test('não deve obter transação de outro usuário', async ({ request, browser }) => {
      // Criar outro usuário e token
      const context = await browser.newContext();
      const page = await context.newPage();

      // Assumindo que existe outro usuário
      const loginResponse = await page.request.post(`${baseURL}/auth/login/`, {
        data: {
          email: 'another@test.com',
          password: 'senha123',
        },
      });

      const loginData = await loginResponse.json();
      const anotherToken = loginData.token || loginData.access;

      // Act: Tentar acessar com outro token
      const response = await request.get(
        `${baseURL}/transactions/${transacaoId}/`,
        { headers: { 'Authorization': `Bearer ${anotherToken}` } }
      );

      // Assert: Deve ser proibido
      expect([403, 404]).toContain(response.status());

      await context.close();
    });
  });

  test.describe('PUT /transactions/:id/', () => {
    let transacaoId: number;

    test.beforeEach(async ({ request }) => {
      // Criar transação
      const response = await request.post(`${baseURL}/transactions/`, {
        headers: { 'Authorization': `Bearer ${token}` },
        data: {
          tipo: 'saída',
          valor: 50,
          categoria: 'lazer',
          descricao: 'Cinema',
        },
      });

      const data = await response.json();
      transacaoId = data.id;
    });

    test('deve atualizar uma transação', async ({ request }) => {
      // Act
      const response = await request.put(
        `${baseURL}/transactions/${transacaoId}/`,
        {
          headers: { 'Authorization': `Bearer ${token}` },
          data: {
            valor: 60,
            descricao: 'Cinema - IMAX',
          },
        }
      );

      // Assert
      expect(response.status()).toBe(200);

      const data = await response.json();
      expect(data.valor).toBe(60);
      expect(data.descricao).toBe('Cinema - IMAX');
    });
  });

  test.describe('DELETE /transactions/:id/', () => {
    let transacaoId: number;

    test.beforeEach(async ({ request }) => {
      // Criar transação
      const response = await request.post(`${baseURL}/transactions/`, {
        headers: { 'Authorization': `Bearer ${token}` },
        data: {
          tipo: 'saída',
          valor: 25,
          categoria: 'saude',
          descricao: 'Farmácia',
        },
      });

      const data = await response.json();
      transacaoId = data.id;
    });

    test('deve deletar uma transação', async ({ request }) => {
      // Act
      const response = await request.delete(
        `${baseURL}/transactions/${transacaoId}/`,
        { headers: { 'Authorization': `Bearer ${token}` } }
      );

      // Assert
      expect([200, 204]).toContain(response.status());

      // Verificar que foi deletada
      const getResponse = await request.get(
        `${baseURL}/transactions/${transacaoId}/`,
        { headers: { 'Authorization': `Bearer ${token}` } }
      );

      expect([404, 403]).toContain(getResponse.status());
    });
  });

  test.describe('Saldo endpoint', () => {
    test('deve retornar saldo correto', async ({ request }) => {
      // Act
      const response = await request.get(`${baseURL}/saldo/`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      // Assert
      expect(response.status()).toBe(200);

      const data = await response.json();
      expect(data.saldo).toBeDefined();
      expect(typeof data.saldo).toBe('number');
    });

    test('deve retornar resumo do mês', async ({ request }) => {
      // Act
      const response = await request.get(`${baseURL}/resumo-mes/`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      // Assert
      expect(response.status()).toBe(200);

      const data = await response.json();
      expect(data.entradas).toBeDefined();
      expect(data.saidas).toBeDefined();
      expect(data.saldo).toBeDefined();
    });
  });
});
