# SisLog - Sistema de Gestão de Logística (STrans)
Projeto-IA - UniSenac
Projeto Final - Inteligência Artificial
Desenvolvimento de Solução IA Integrada para Empresas

Este projeto final tem como objetivo integrar os conhecimentos de IA com desenvolvimento prático:
- Aplicar técnicas de IA para resolver problemas empresariais reais
- Desenvolver interface funcional que exponha a solução
- Integrar modelos de IA com front-end utilizável
- Aproveitar conhecimentos de outras disciplinas do curso
- Criar solução que agregue valor real ao negócio
- Demonstrar viabilidade técnica e comercial da solução

📖 __Sobre o Projeto__
O SisLog é um sistema web, desenvolvido como um projeto prático para demonstrar a integração de tecnologias de desenvolvimento web, análise de dados e Machine Learning. 
A aplicação permite a visualização de dados operacionais, a geração de análises gráficas e a otimização de rotas de coleta utilizando a API do Google Maps.
Este projeto foi construído com Python e o microframework Flask, e foi projetado para ser modular, seguro e escalável.

✨ __Funcionalidades Principais__
🔐 **Sistema de Autenticação:** 
Tela de login segura que valida as credenciais do usuário a partir de um banco de dados de usuários.
👤 **Gerenciamento de Sessão:** 
O acesso às páginas internas é protegido e requer login.
📊 **Visualização de Dados (Browse):** 
Telas para visualização de dados operacionais de Clientes, Veículos, Rotas, Entregas e Coletas, com sistema de filtro dinâmico.
🧠 **Análise de Clientes com Machine Learning:** 
Utiliza o algoritmo K-Means Clustering para classificar clientes em 3 níveis de volume (Baixo, Médio, Alto), gerando gráficos comparativos por tipo de cliente, porte e região.
📈 **Análise de Entregas e Veículos:** 
Gera gráficos de comparação anual e evolução mensal do volume de entregas. Utiliza Regressão Linear para prever tendências de desempenho para diferentes tipos de veículos.
🗺️ **Otimização de Rota de Coletas:**
Permite a seleção de múltiplas coletas em uma interface interativa.Utiliza a API do Google Maps para calcular a rota mais eficiente entre um ponto de partida, os pontos de coleta selecionados e um destino final.Gerencia permissões de usuário para decidir entre o uso da API paga (otimização real) ou uma API simulada (gratuita).Exibe o roteiro otimizado em uma tabela e permite a visualização direta no Google Maps.
📝 **Auditoria de API:** 
Salva os dados de envio e retorno da API de otimização em arquivos de texto para fins de auditoria e depuração.

🛠️ __Tecnologias Utilizadas__
**Backend:** Python
**Framework Web:** Flask
**Análise de Dados:** Pandas
**Machine Learning:** Scikit-learn (KMeans, LinearRegression)
**Geração de Gráficos:** Matplotlib, Seaborn
**Frontend:** HTML5, CSS3, JavaScript
**Otimização de Rotas:** Google Maps Directions API
**Gerenciamento de Segredos:** Python-dotenv

