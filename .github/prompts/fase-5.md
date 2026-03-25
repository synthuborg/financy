**Contexto Inicial Obrigatório:** Leia as diretrizes em `.github/copilot/instrucoes-gerais/`, `.github/skills/` e `.github/agents/`. Esta fase consolida a entrega obrigatória e os diferenciais do hackathon.

**Objetivo:** Criar o painel gerencial e implementar filtros de pesquisa robustos.

**Tarefas:**
1. No app `dashboard`, crie a view principal que consome `calculate_balance` e renderiza um resumo financeiro limpo (Saldo Atual, Entradas, Saídas).
2. Volte ao `selectors.py` e adicione parâmetros opcionais de filtro (por período de datas, busca textual por descrição ou filtro por categoria).
3. Integre esses filtros na view de listagem de transações e crie a interface de busca no template HTML correspondente.
4. Adicione tratamento de erros visuais (messages framework do Django) para informar o usuário sobre ações bem-sucedidas ou erros de formulário.

**Ação Final Obrigatória:** Execute todos os testes do projeto. Revise o código para garantir que não há dados sensíveis expostos. Adicione um "Checklist de Entrega Base" ao `README.md` comprovando o cumprimento de todos os requisitos do regulamento. Fixe o passo a passo final para a banca avaliar o projeto.