**Contexto Inicial Obrigatório:** Consulte `.github/copilot/instrucoes-gerais/`, `.github/skills/` e `.github/agents/` para manter o padrão de código e UI estabelecidos.

**Objetivo:** Construir a interface de usuário focada em usabilidade mobile-first e conectar a lógica de domínio ao Django Templates.

**Tarefas:**
1. Crie os formulários baseados em modelos (`forms.py`) para `Transaction` e `Category`, incluindo classes CSS e validações amigáveis.
2. Desenvolva as views no app `finances` (Listar, Criar, Editar, Excluir). **Atenção:** as views devem ser enxutas. Elas extraem os dados do `request`, repassam para as funções do `services.py` e renderizam os templates com os dados do `selectors.py`.
3. Crie os templates HTML com foco total em mobile-first, garantindo tabelas/listas responsivas e botões acessíveis em telas de celular.
4. Crie testes de integração (Client test) verificando o fluxo de navegação e os status codes (200, 302).

**Ação Final Obrigatória:** Execute a suíte de testes de integração. Atualize o `README.md` descrevendo as decisões de design responsivo e detalhando as rotas (URLs) disponíveis até o momento.