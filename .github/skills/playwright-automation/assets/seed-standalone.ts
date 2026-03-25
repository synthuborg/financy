// tests/scripts/seed-standalone.ts
import { chromium } from '@playwright/test';
import { SeedDataHelper } from '../helpers/seed-data';

/**
 * Script standalone para popular banco de dados via UI
 * 
 * Pode ser executado:
 * ts-node tests/scripts/seed-standalone.ts
 * ou
 * npm run seed:data
 */
async function seedDatabase() {
  console.log('🚀 Iniciando script de seed de dados...\n');

  const browser = await chromium.launch({ headless: false }); // headless: false para ver
  const context = await browser.createIncognitoBrowserContext();
  const page = await context.newPage();

  try {
    // 1. Navegar para dashboard
    console.log('📍 Acessando dashboard...');
    await page.goto('http://localhost:8000/dashboard/', { timeout: 10000 });

    // 2. Fazer login se necessário
    const isLoggedIn = await page.url().includes('dashboard');
    if (!isLoggedIn) {
      console.log('🔐 Fazendo login...');
      
      await page.fill('input[type="email"]', 'user@test.com');
      await page.fill('input[type="password"]', 'senha123');
      await page.click('button:has-text("Entrar")');
      
      await page.waitForURL('**/dashboard/**');
      console.log('✅ Login realizado!');
    }

    // 3. Popular dados
    console.log('\n📝 Populando banco de dados...\n');
    
    const seeder = new SeedDataHelper(page);
    
    // Opção 1: Dados predefinidos (rápido e previsível)
    // await seeder.populatePredefinedData();
    
    // Opção 2: Dados aleatórios (mais realista)
    await seeder.populateTestData(15);

    console.log('\n✅ Seed concluído com sucesso!');
    
    // 4. Manter browser aberto por 5 segundos para confirmar
    console.log('\n👀 Navegador fechará automaticamente em 5 segundos...');
    await page.waitForTimeout(5000);

  } catch (error) {
    console.error('\n❌ Erro durante seed:', error);
    process.exit(1);
  } finally {
    await browser.close();
    console.log('🎉 Done!\n');
  }
}

// Executar se for chamado diretamente
if (require.main === module) {
  seedDatabase().catch(console.error);
}

export default seedDatabase;
