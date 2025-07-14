## SisLog - Sistema de Gestão de Logística (STrans)
#Projeto-IA - UniSenac
#Projeto Final - Inteligência Artificial

Desenvolvimento de Solução IA Integrada para Empresas

Este projeto final tem como objetivo integrar os conhecimentos de IA com desenvolvimento prático:
- Aplicar técnicas de IA para resolver problemas empresariais reais
- Desenvolver interface funcional que exponha a solução
- Integrar modelos de IA com front-end utilizável
- Aproveitar conhecimentos de outras disciplinas do curso
- Criar solução que agregue valor real ao negócio
- Demonstrar viabilidade técnica e comercial da solução


__Funcionalidades Principais__
- **Sistema de Autenticação:** Tela de login segura que valida a partir de um banco de dados de usuários.
- **Gerenciamento de Sessão:** O acesso às páginas internas é protegido e requer login.
- **Visualização de Dados (Browse):** Telas para visualização de dados operacionais de Clientes, Veículos, Rotas, Entregas e Coletas, com sistema de filtro dinâmico.
- **Análise de Clientes com Machine Learning:** Utiliza o algoritmo K-Means Clustering para classificar clientes, gerando gráficos.
- **Análise de Entregas e Veículos:** Gera gráficos de comparação anual e evolução mensal do volume de entregas. Utiliza Regressão Linear para prever tendências de desempenho para diferentes tipos de veículos.
- **Otimização de Rota de Coletas:** 
	-- Permite a seleção de múltiplas coletas em uma interface interativa. 
	-- Utiliza a API do Google Maps para calcular a rota mais eficiente entre um ponto de partida, os pontos de coleta selecionados e um destino final.
	-- Gerencia permissões de usuário para decidir entre o uso da API paga (otimização real) ou uma API simulada (gratuita).
	-- Exibe o roteiro otimizado em uma tabela e permite a visualização direta no Google Maps.
