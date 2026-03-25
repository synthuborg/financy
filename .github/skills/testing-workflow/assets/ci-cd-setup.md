# CI/CD Setup - Integração Contínua & Deploy

Configurar GitHub Actions para executar testes automaticamente e deploy seguro.

## Estrutura de Arquivos

```
.github/workflows/
├── test.yml           # Roda testes em cada push
├── e2e-nightly.yml    # E2E completo à noite
└── deploy.yml         # Deploy após testes passarem
```

## 1. Workflow de Testes (test.yml)

Criar `.github/workflows/test.yml`:

```yaml
name: 🧪 Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    name: Test Suite
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - name: ✅ Checkout code
        uses: actions/checkout@v4
      
      - name: 📦 Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: 🐍 Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: 📥 Install dependencies
        run: |
          npm ci
          pip install -r requirements.txt
          npx playwright install --with-deps
      
      - name: 🗄️ Setup database
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
          DJANGO_SETTINGS_MODULE: config.settings.test
        run: |
          python manage.py migrate
          python manage.py createsuperuser --noinput --username testuser --email test@test.com || true
      
      - name: 🚀 Start Django
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
          DJANGO_SETTINGS_MODULE: config.settings.test
        run: |
          python manage.py runserver &
          sleep 3
      
      - name: 🧪 Run API Tests
        run: npm run test:api
      
      - name: 🎭 Run E2E Tests
        run: npm run test:e2e
      
      - name: 📊 Generate Report
        if: always()
        run: npx playwright show-report
      
      - name: 📤 Upload Coverage
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
      
      - name: 💥 Test Failed Alert
        if: failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Testes falharam! Veja [report](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }})'
            })
```

## 2. E2E Nightly (e2e-nightly.yml)

Criar `.github/workflows/e2e-nightly.yml`:

```yaml
name: 🌙 Nightly E2E Tests

on:
  schedule:
    # Rodar toda noite às 2am UTC (23h BRT)
    - cron: '0 2 * * *'
  workflow_dispatch: # Manual trigger

jobs:
  nightly:
    name: Full E2E Suite
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: nightly_db
          POSTGRES_USER: nightly_user
          POSTGRES_PASSWORD: nightly_pass
        ports:
          - 5432:5432
    
    steps:
      - name: ✅ Checkout code
        uses: actions/checkout@v4
      
      - name: 📦 Setup Node & Python
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: 📥 Install dependencies
        run: |
          npm ci
          pip install -r requirements.txt
          npx playwright install --with-deps
      
      - name: 🗄️ Setup & Seed database
        env:
          DATABASE_URL: postgresql://nightly_user:nightly_pass@localhost:5432/nightly_db
        run: |
          python manage.py migrate
          npm run seed:data  # Usar Playwright automation para seed
      
      - name: 🚀 Start Django
        env:
          DATABASE_URL: postgresql://nightly_user:nightly_pass@localhost:5432/nightly_db
        run: |
          python manage.py runserver 0.0.0.0:8000 &
          sleep 5
      
      - name: 🧪 Run Full E2E
        run: |
          npx playwright test tests/e2e \
            --reporter=html,github,json \
            --headed  # Usar navegador completo para melhor debug
      
      - name: 📊 Generate Report
        if: always()
        run: npx playwright show-report
      
      - name: 📤 Upload Report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: e2e-report-nightly
          path: playwright-report/
          retention-days: 90
      
      - name: 📧 Email Report
        if: always()
        uses: davispeterson/action-send-email@main
        with:
          server_address: ${{ secrets.EMAIL_SERVER }}
          server_port: ${{ secrets.EMAIL_PORT }}
          username: ${{ secrets.EMAIL_USER }}
          password: ${{ secrets.EMAIL_PASS }}
          subject: 'E2E Nightly Report - ${{ job.status }}'
          to: 'team@example.com'
          from: 'ci@example.com'
          body: |
            E2E Nightly test report
            Status: ${{ job.status }}
            Report: https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

## 3. Deploy Workflow (deploy.yml)

Criar `.github/workflows/deploy.yml`:

```yaml
name: 🚀 Deploy

on:
  push:
    branches: [main]
  workflow_run:
    workflows: ["🧪 Tests"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    if: github.event.workflow_run.conclusion == 'success' || github.event_name == 'push'
    
    environment:
      name: production
      url: https://app.example.com
    
    steps:
      - name: ✅ Checkout code
        uses: actions/checkout@v4
      
      - name: 🔑 Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: arn:aws:iam::ACCOUNT:role/github-actions
          aws-region: us-east-1
      
      - name: 📦 Setup environment
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: 🧹 Collect static files
        env:
          SECRET_KEY: ${{ secrets.SECRET_KEY }}
          DEBUG: 'False'
        run: |
          pip install -r requirements.txt
          python manage.py collectstatic --noinput
      
      - name: 📤 Upload to S3
        run: |
          aws s3 sync static/ s3://my-bucket/static/ \
            --delete \
            --cache-control "max-age=31536000"
      
      - name: 🐳 Build Docker image
        run: docker build -t my-app:${{ github.sha }} .
      
      - name: 🏢 Push to ECR
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin ${{ secrets.AWS_ECR_URI }}
          docker tag my-app:${{ github.sha }} ${{ secrets.AWS_ECR_URI }}/my-app:latest
          docker push ${{ secrets.AWS_ECR_URI }}/my-app:latest
      
      - name: 🎯 Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster production \
            --service my-app \
            --force-new-deployment \
            --region us-east-1
      
      - name: ✅ Verify deployment
        run: |
          sleep 30
          curl -f https://app.example.com/health || exit 1
      
      - name: 📱 Notify Slack
        if: always()
        uses: slackapi/slack-github-action@v1.24.0
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "Deployment Status: ${{ job.status }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Deploy Report*\nStatus: ${{ job.status }}\nCommit: ${{ github.sha }}\nAuthor: ${{ github.actor }}\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Details>"
                  }
                }
              ]
            }
```

## Configurar Secrets

No GitHub repo settings (`Settings → Secrets and variables → Actions`):

```
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
AWS_ECR_URI=123456.dkr.ecr.us-east-1.amazonaws.com
SLACK_WEBHOOK=https://hooks.slack.com/services/...
EMAIL_SERVER=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=ci@example.com
EMAIL_PASS=app-password
```

## Branch Protection

Em `Settings → Branches → Main branch`:

```
✓ Require a pull request before merging
✓ Require status checks to pass:
  - Test Suite
  - Full E2E Suite (se aplicável)
✓ Require branches to be up to date
✓ Require conversation resolution
```

## Local Testing Do Workflow

### Simular CI Localmente

```bash
# Instalar act (GitHub Actions local runner)
brew install act  # Mac
# ou download: https://github.com/nektos/act

# Rodar workflow test.yml
act push -j test

# Rodar com debug
act push -j test -v
```

### Testar sem CI/CD

```bash
# Setup local
npm ci
pip install -r requirements.txt
npx playwright install --with-deps

# Rodar como CI
npm run test:api
npm run test:e2e
```

## Monitoring & Alerts

### Health Check Endpoint

Django `urls.py`:

```python
def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'version': '1.0.0',
        'timestamp': now(),
    })

urlpatterns = [
    path('health/', health_check),
]
```

### Slack Notifications

Adicione ao workflow antes de qualquer step:

```yaml
- name: Send to Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "❌ Build Failed",
        "link": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
      }
```

### Email Notification

```yaml
- name: Send Email
  if: always()
  uses: davispeterson/action-send-email@main
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: 'CI/CD Report: ${{ job.status }}'
    to: team@example.com
    body: |
      Tests: ${{ job.status }}
      Commit: ${{ github.sha }}
      Branch: ${{ github.ref_name }}
      Details: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

## Performance Optimization

### Cache Dependencies

```yaml
- name: Cache npm
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}

- name: Cache pip
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

- name: Cache Playwright
  uses: actions/cache@v3
  with:
    path: ~/.cache/ms-playwright
    key: ${{ runner.os }}-playwright-${{ hashFiles('**/package-lock.json') }}
```

### Parallel Jobs

```yaml
jobs:
  test-api:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:api

  test-e2e:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:e2e

  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint
```

## Troubleshooting CI/CD

### Timeout do Playwright

```yaml
- name: Run E2E with longer timeout
  run: npm run test:e2e -- --timeout=60000
```

### Database Connection

```yaml
- name: Wait for Postgres
  run: |
    until pg_isready -h localhost -p 5432; do
      echo 'waiting for postgres...'
      sleep 1
    done
```

### Django Not Ready

```yaml
- name: Wait for Django
  run: |
    for i in {1..30}; do
      if curl -f http://localhost:8000; then exit 0; fi
      sleep 1
    done
    exit 1
```

## Próximos Passos

1. [Setup Ambiente Local](setup-guide.md)
2. [Estratégia de Testes](testing-strategy.md)
3. [Debugging Avançado](debugging-guide.md)
4. Usar [Playwright Automation Skills](link-to-skill:/playwright-automation) para data population

## Referências

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Playwright CI Setup](https://playwright.dev/python/docs/ci)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
