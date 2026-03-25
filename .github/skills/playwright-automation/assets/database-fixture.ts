// tests/fixtures/database.fixture.ts
import { test as base } from '@playwright/test';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

type DatabaseFixtures = {
  cleanDatabase: void;
  freshDatabase: void;
};

/**
 * Fixtures para gerenciar banco de dados durante testes
 */
export const test = base.extend<DatabaseFixtures>({
  cleanDatabase: async ({}, use) => {
    // Setup: Não fazer nada, apenas avisar
    console.log('🧹 Limpando banco de dados...');

    await use();

    // Teardown: Deletar todas as transações de teste
    try {
      // Via Django shell
      await execAsync(
        'python manage.py shell -c "from myapp.models import Transaction; Transaction.objects.filter(descricao__startswith=\'Transação teste\').delete()"'
      );
      console.log('✅ Banco de dados limpo!');
    } catch (error) {
      console.error('❌ Erro ao limpar banco:', error);
    }
  },

  freshDatabase: async ({}, use) => {
    // Setup: Reset banco completo
    try {
      console.log('🔄 Resetando banco de dados...');
      
      // Rodar migrations
      await execAsync('python manage.py migrate --noinput');
      
      // Criar usuário de teste
      await execAsync(
        'python manage.py shell -c "' +
        'from django.contrib.auth import get_user_model; ' +
        'User = get_user_model(); ' +
        'User.objects.filter(email=\"test@test.com\").delete(); ' +
        'User.objects.create_user(email=\"test@test.com\", password=\"senha123\")' +
        '"'
      );

      console.log('✅ Banco fresco criado com usuário de teste!');
    } catch (error) {
      console.error('❌ Erro ao resetar banco:', error);
    }

    await use();

    // Teardown: Limpar dados de teste
    try {
      await execAsync(
        'python manage.py shell -c "' +
        'from django.contrib.auth import get_user_model; ' +
        'User = get_user_model(); ' +
        'User.objects.filter(email=\"test@test.com\").delete()' +
        '"'
      );
    } catch (error) {
      console.error('❌ Erro no teardown:', error);
    }
  },
});

export { expect } from '@playwright/test';
