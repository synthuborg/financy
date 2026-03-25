**Contexto Inicial Obrigatório:** Antes de gerar qualquer código ou iniciar esta tarefa, leia atentamente e assimile todas as diretrizes presentes nos arquivos das pastas `.github/copilot/instrucoes-gerais/`, `.github/skills/` e `.github/agents/`. A sua execução deve ser estritamente guiada pelas regras, skills e comportamentos definidos nesses arquivos.

**Atuação:** Atue como um Engenheiro de Software Sênior especialista em Python, Django e Arquitetura Limpa. 

**Objetivo:** Iniciar o projeto de gestão financeira do hackathon "Ctrl+Alt+AI" (equipe JRD Labs). A stack é Python, Django, SQLite, templates nativos e CSS mobile-first (zero uso de DRF ou Docker).

**Tarefas:**
1. Crie a estrutura inicial do projeto Django garantindo a separação em múltiplos apps: `core` (configurações gerais), `finances` (domínio de transações) e `dashboard` (apresentação de resumos).
2. Implemente o alicerce da Arquitetura Limpa: dentro de cada app, crie os arquivos `services.py` (para mutações e regras de negócio) e `selectors.py` (para consultas ao banco). 
3. Regra de Ouro: **Nenhuma regra de negócio ou query complexa deve existir no `views.py`**. As views atuam apenas como controladores HTTP.
4. Crie os testes automatizados básicos para garantir que a infraestrutura inicial e o roteamento estão operantes.

**Ação Final Obrigatória:** Execute a suíte de testes. Crie um arquivo `README.md` curador e completo para o time. Este README deve conter: instruções exatas para rodar o projeto localmente, a explicação da estrutura de pastas adotada (focada em Clean Architecture) e o registro do andamento desta Fase 1.