## SisLog - Sistema de Gestão de Logística (STrans)
### Projeto-IA - UniSenac
### Projeto Final - Inteligência Artificial

### ___Autores:___
- ***Fábio Briddi*** - Desenvovimento e Conceito
- ***Gustavo Casarin*** - Desenvovimento e Documentação

### ___Objetivo:___
Desenvolvimento de Solução IA Integrada para Empresas

Este projeto final tem como objetivo integrar os conhecimentos de IA com desenvolvimento prático:
- Aplicar técnicas de IA para resolver problemas empresariais reais
- Desenvolver interface funcional que exponha a solução
- Integrar modelos de IA com front-end utilizável
- Aproveitar conhecimentos de outras disciplinas do curso
- Criar solução que agregue valor real ao negócio
- Demonstrar viabilidade técnica e comercial da solução


### ___Funcionalidades Principais___
- **Sistema de Autenticação:** Tela de login segura que valida a partir de um banco de dados de usuários.
- **Gerenciamento de Sessão:** O acesso às páginas internas é protegido e requer login.
- **Visualização de Dados (Browse):** Telas para visualização de dados operacionais de Clientes, Veículos, Rotas, Entregas e Coletas, com sistema de filtro dinâmico.
- **Análise de Clientes com Machine Learning:** Utiliza o algoritmo K-Means Clustering para classificar clientes, gerando gráficos.
- **Análise de Entregas e Veículos:** Gera gráficos de comparação anual e evolução mensal do volume de entregas. Utiliza Regressão Linear para prever tendências de desempenho para diferentes tipos de veículos.
- **Otimização de Rota de Coletas:** 
	- Permite a seleção de múltiplas coletas em uma interface interativa. 
	- Utiliza a API do Google Maps para calcular a rota mais eficiente entre um ponto de partida, os pontos de coleta selecionados e um destino final.
	- Gerencia permissões de usuário para decidir entre o uso da API paga (otimização real) ou uma API simulada (gratuita).
	- Exibe o roteiro otimizado em uma tabela e permite a visualização direta no Google Maps.

### ___Tecnologias Utilizadas___
- **Backend:** Python
- **Framework Web:** Flask
- **Análise de Dados:** Pandas
- **Machine Learning:** Scikit-learn (KMeans, LinearRegression)
- **Geração de Gráficos:** Matplotlib, Seaborn
- **Frontend:** HTML5, CSS3, JavaScript
- **Otimização de Rotas:** Google Maps Directions API
- **Gerenciamento de Dados Sensíveis (Chave Secreta):** Python-dotenv

### ___Como Executar o Projeto___

1. **Pré-requisitos:**
   - Python 3.8 ou superior instalado.
   - Git instalado.
2. **Configuração do Ambiente:**
   - Clone o repositório (ou use sua pasta local):
      - ` git clone https://github.com/seu-usuario/seu-repositorio.git
      - ` cd seu-repositorio
   - Crie e ative um ambiente virtual:
      - ` python -m venv venv
      - ` .\venv\Scripts\activate
   - Instale as dependências:
      - ` pip install -r requirements.txt
   - Configure a Chave da API (Opcional):
      - Na pasta raiz do projeto, crie um arquivo chamado: ` .env.
      - Abra o arquivo `.env` e adicione a seguinte linha, substituindo pela sua chave real da API do Google Maps: ` GOOGLE_MAPS_API_KEY="SUA_CHAVE_DE_API_REAL_VAI_AQUI"
      - **Observação:** O arquivo ` .env ` está listado no .gitignore, então sua chave secreta nunca será enviada para o repositório.
   - Estrutura de Dados:
      - Certifique-se de que a pasta ` C:\suapasta\STRANS-Projeto-IA\DataSets ` existe ou ajuste o caminho no arquivo app.py.
      - Garanta que todos os arquivos ` .csv `  necessários estejam dentro desta pasta.
3. **Execução:**
   - Com o ambiente virtual ativado, execute o seguinte comando no terminal:
     ` flask run
   - Abra o navegador e acesse o endereço:
     ` http://127.0.0.1:5000
   - Use as credenciais abaixo para fazer login:
     - Login: ` admin
     - Senha: ` q1w2e3r4
