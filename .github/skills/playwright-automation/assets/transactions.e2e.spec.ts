// tests/e2e/transactions.e2e.spec.ts
import { test, expect } from '../fixtures/auth.fixture';
import { SeedDataHelper } from '../helpers/seed-data';

test.describe('Transações - E2E Tests', () => {
  
  test.describe('Adicionar Transação', () => {
    test('deve adicionar uma saída com sucesso', async ({ authenticatedPage: page }) => {
      // Arrange
      await page.goto('/dashboard/');
      const saldoAntes = await page.locator('text="R\\$ 2.450,50"').first();
      const saldoAntesText = await saldoAntes.textContent();

      // Act: Abrir modal
      await page.click('button:has-text("+ Adicionar")');
      await expect(page.locator('#modalTransacao')).toBeVisible();

      // Selecionar saída
      await page.click('button:has-text("Saída")');

      // Preencher formulário
      await page.fill('input[name="valor"]', '85.50');
      await page.selectOption('select[name="categoria"]', 'alimentacao');
      await page.fill('input[name="data"]', '2024-03-25');
      await page.fill('input[name="descricao"]', 'Supermercado Extra');

      // Salvar
      await page.click('button:has-text("Salvar")');

      // Assert
      await expect(page.locator('text=Transação salva com sucesso')).toBeVisible();
      await expect(page.locator('text=Supermercado Extra')).toBeVisible();
      
      // Verificar saldo atualizou
      const saldoDepois = await page.locator('text="R\\$ 2.365"').first();
      await expect(saldoDepois).toBeVisible();
    });

    test('deve adicionar uma entrada com sucesso', async ({ authenticatedPage: page }) => {
      // Arrange
      await page.goto('/dashboard/');

      // Act
      await page.click('button:has-text("+ Adicionar")');
      await page.click('button:has-text("Entrada")');
      await page.fill('input[name="valor"]', '500');
      await page.selectOption('select[name="categoria"]', 'renda');
      await page.fill('input[name="descricao"]', 'Freelance');
      await page.click('button:has-text("Salvar")');

      // Assert
      await expect(page.locator('text=Freelance')).toBeVisible();
      await expect(page.locator('text=\\+R\\$ 500').first()).toBeVisible();
    });

    test('não deve salvar com valor vazio', async ({ authenticatedPage: page }) => {
      // Arrange
      await page.goto('/dashboard/');

      // Act
      await page.click('button:has-text("+ Adicionar")');
      
      // Tentar salvar sem valor
      await page.click('button:has-text("Salvar")');

      // Assert: Input deve ter erro/estar required
      const valorInput = page.locator('input[name="valor"]');
      const validity = await valorInput.evaluate(el => (el as HTMLInputElement).validity.valid);
      expect(validity).toBe(false);
    });
  });

  test.describe('Filtrar Transações', () => {
    test('deve filtrar por mês', async ({ authenticatedPage: page }) => {
      // Arrange
      await page.goto('/dashboard/');
      
      // Adicionar algumas transações
      const seeder = new SeedDataHelper(page);
      await seeder.populatePredefinedData();

      // Act: Filtrar por mês específico
      await page.selectOption('select[name="mes"]', '03');
      
      // Aguardar atualização (debounce)
      await page.waitForTimeout(500);

      // Assert: URL deve ter query param
      expect(page.url()).toContain('mes=03');
      
      // Transações devem estar visíveis
      await expect(page.locator('text=Supermercado')).toBeVisible();
    });

    test('deve filtrar por categoria', async ({ authenticatedPage: page }) => {
      // Arrange
      await page.goto('/dashboard/');

      // Act
      await page.selectOption('select[name="categoria"]', 'alimentacao');
      await page.waitForTimeout(500);

      // Assert
      expect(page.url()).toContain('categoria=alimentacao');
      
      // Apenas transações de alimentação devem aparecer
      const transacoes = await page.locator('[data-category="alimentacao"]').count();
      expect(transacoes).toBeGreaterThan(0);
    });

    test('deve limpar filtros', async ({ authenticatedPage: page }) => {
      // Arrange
      await page.goto('/dashboard/?mes=03&categoria=alimentacao');

      // Act
      await page.click('button:has-text("Limpar")');

      // Assert
      expect(page.url()).toBe('http://localhost:8000/dashboard/');
      
      // Todos os selects devem estar vazios
      const mesSelect = page.locator('select[name="mes"]');
      const categoriaSelect = page.locator('select[name="categoria"]');
      
      expect(await mesSelect.inputValue()).toBe('');
      expect(await categoriaSelect.inputValue()).toBe('');
    });
  });

  test.describe('Editar/Deletar Transação', () => {
    test('deve editar uma transação', async ({ authenticatedPage: page }) => {
      // Arrange
      await page.goto('/dashboard/');
      
      // Adicionar transação
      const seeder = new SeedDataHelper(page);
      await seeder.addTransaction({
        tipo: 'saída',
        valor: 50,
        categoria: 'alimentacao',
        descricao: 'Original',
      });

      // Act: Clicar em transação para editar
      await page.click('text=Original');
      await page.fill('input[name="descricao"]', 'Editada');
      await page.click('button:has-text("Salvar")');

      // Assert
      await expect(page.locator('text=Editada')).toBeVisible();
      await expect(page.locator('text=Original')).not.toBeVisible();
    });

    test('deve deletar uma transação com confirmação', async ({ authenticatedPage: page }) => {
      // Arrange
      await page.goto('/dashboard/');
      
      const seeder = new SeedDataHelper(page);
      await seeder.addTransaction({
        tipo: 'saída',
        valor: 30,
        categoria: 'lazer',
        descricao: 'Para deletar',
      });

      // Act
      await page.click('text=Para deletar');
      await page.click('button:has-text("Deletar")');
      
      // Confirmar deleção
      await page.click('button:has-text("Confirmar")');

      // Assert
      await expect(page.locator('text=Para deletar')).not.toBeVisible();
    });
  });

  test.describe('Gráfico de Categorias', () => {
    test('deve mostrar distribuição correta de gastos', async ({ authenticatedPage: page }) => {
      // Arrange
      await page.goto('/dashboard/');
      
      const seeder = new SeedDataHelper(page);
      await seeder.populatePredefinedData();

      // Assert: Verificar se gráfico está presente
      await expect(page.locator('text=Gastos por Categoria')).toBeVisible();
      
      // Verificar percentuais
      await expect(page.locator('text=Alimentação')).toBeVisible();
      await expect(page.locator('text=Transporte')).toBeVisible();
    });
  });
});
