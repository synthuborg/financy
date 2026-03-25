// tests/helpers/seed-data.ts
import { Page, expect } from '@playwright/test';

export interface TransactionData {
  tipo: 'entrada' | 'saída';
  valor: number;
  categoria: string;
  descricao?: string;
  data?: string;
}

/**
 * Helper para automação de dados via UI
 * Simula um usuário adicionando transações
 */
export class SeedDataHelper {
  constructor(private page: Page) {}

  /**
   * Adiciona uma transação através da UI
   */
  async addTransaction(data: TransactionData) {
    // Abrir modal de adicionar
    await this.page.click('button:has-text("+ Adicionar")');
    
    // Aguardar modal estar visível
    const modal = this.page.locator('#modalTransacao');
    await expect(modal).toBeVisible();

    // Selecionar tipo (entrada ou saída)
    const tipoButton = this.page.locator('button:has-text("' + 
      (data.tipo === 'entrada' ? 'Entrada' : 'Saída') + '")');
    await tipoButton.click();

    // Preencher valor
    await this.page.fill('input[name="valor"]', data.valor.toString());

    // Selecionar categoria
    await this.page.selectOption('select[name="categoria"]', data.categoria);

    // Preencher data (ou usar today)
    if (data.data) {
      await this.page.fill('input[name="data"]', data.data);
    }

    // Preencher descrição (opcional)
    if (data.descricao) {
      const descInput = this.page.locator('input[name="descricao"]');
      await descInput.fill(data.descricao);
    }

    // Clicar em salvar
    await this.page.click('button:has-text("Salvar")');

    // Aguardar sucesso
    await expect(this.page.locator('text=Transação salva')).toBeVisible();
    
    // Aguardar animação/atualização
    await this.page.waitForTimeout(500);
  }

  /**
   * Popula banco de dados com transações aleatórias
   */
  async populateTestData(count: number = 10) {
    const categorias = ['alimentacao', 'transporte', 'saude', 'lazer', 'utilitarios'];
    const descricoes = [
      'Supermercado',
      'Uber/Táxi',
      'Farmácia',
      'Cinema',
      'Conta de água',
      'Netflix',
      'Salão de beleza',
      'Academia',
      'Restaurante',
      'Posto de gasolina',
    ];

    for (let i = 0; i < count; i++) {
      const tipo = Math.random() > 0.7 ? 'entrada' : 'saída';
      const valor = tipo === 'entrada' 
        ? Math.floor(Math.random() * 5000) + 1000
        : Math.floor(Math.random() * 500) + 10;
      const categoria = categorias[Math.floor(Math.random() * categorias.length)];
      const descricao = descricoes[Math.floor(Math.random() * descricoes.length)];

      console.log(`📝 Adicionando transação ${i + 1}/${count}: ${descricao} (${tipo})`);

      await this.addTransaction({
        tipo,
        valor,
        categoria,
        descricao,
      });
    }

    console.log(`✅ ${count} transações adicionadas com sucesso!`);
  }

  /**
   * Popula com dados específicos (para testes previsíveis)
   */
  async populatePredefinedData() {
    const transactions = [
      {
        tipo: 'entrada' as const,
        valor: 3500,
        categoria: 'renda',
        descricao: 'Salário mensal',
      },
      {
        tipo: 'entrada' as const,
        valor: 500,
        categoria: 'renda',
        descricao: 'Freelance',
      },
      {
        tipo: 'saída' as const,
        valor: 150,
        categoria: 'alimentacao',
        descricao: 'Supermercado',
      },
      {
        tipo: 'saída' as const,
        valor: 80,
        categoria: 'transporte',
        descricao: 'Uber para trabalho',
      },
      {
        tipo: 'saída' as const,
        valor: 30,
        categoria: 'lazer',
        descricao: 'Netflix',
      },
      {
        tipo: 'saída' as const,
        valor: 200,
        categoria: 'saude',
        descricao: 'Consulta médica',
      },
      {
        tipo: 'saída' as const,
        valor: 120,
        categoria: 'utilitarios',
        descricao: 'Conta de água',
      },
    ];

    for (const transaction of transactions) {
      console.log(`📝 Adicionando: ${transaction.descricao}`);
      await this.addTransaction(transaction);
    }

    console.log(`✅ Dados predefinidos adicionados!`);
  }
}

/**
 * Função helper para usar rapidamente em testes
 */
export async function populateDatabaseUI(page: Page, count: number = 10) {
  const seeder = new SeedDataHelper(page);
  await seeder.populateTestData(count);
}

export async function populatePredefinedDataUI(page: Page) {
  const seeder = new SeedDataHelper(page);
  await seeder.populatePredefinedData();
}
