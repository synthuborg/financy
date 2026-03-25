// tests/fixtures/auth.fixture.ts
import { test as base, Page, expect } from '@playwright/test';

type AuthFixtures = {
  authenticatedPage: Page;
  unauthenticatedPage: Page;
};

/**
 * Fixture de autenticação
 * Fornece uma página já logada para testes
 */
export const test = base.extend<AuthFixtures>({
  authenticatedPage: async ({ page }, use) => {
    // Setup: Fazer login
    await page.goto('/login/');
    
    // Preencher credenciais de teste
    await page.fill('input[type="email"]', 'user@test.com');
    await page.fill('input[type="password"]', 'senha123');
    await page.click('button:has-text("Entrar")');
    
    // Aguardar redirecionamento para dashboard
    await page.waitForURL('**/dashboard/**');
    
    // Aguardar dashboard carregar completamente
    await page.waitForLoadState('networkidle');
    
    // Fornecer página autenticada para o teste
    await use(page);
    
    // Teardown: Logout (opcional, browser fecha mesmo)
    try {
      await page.click('button:has-text("Logout")');
    } catch (e) {
      // Se não encontrar botão, tudo bem
    }
  },

  unauthenticatedPage: async ({ page }, use) => {
    // Página sem autenticação
    await use(page);
  },
});

export { expect } from '@playwright/test';
