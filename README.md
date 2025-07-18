# 🚚 SisLog - Sistema de Gestão de Logística Inteligente para Transportadoras (STRANS)

## Visão Geral do Projeto

O **SisLog** é uma solução inovadora de gestão de logística desenvolvida para otimizar as operações de transportadoras por meio da **Inteligência Artificial (IA)**. Este projeto integra funcionalidades de gerenciamento operacional com análise de dados avançada e otimização de rotas, proporcionando uma ferramenta robusta para o planejamento, execução e análise de atividades logísticas.

## ✨ Destaques do Projeto

*   **Inteligência Artificial Aplicada:** Utilização de modelos de Machine Learning para análise de clientes, previsão de tendências de entregas e otimização de rotas.
*   **Otimização de Rotas Avançada:** Integração com a API do Google Maps para cálculo de rotas de coletas mais eficientes, com exibição interativa.
*   **Interface Web Intuitiva:** Desenvolvido com Flask, oferece um ambiente de fácil navegação para todas as funcionalidades.
*   **Segurança Robusta:** Sistema de autenticação e gerenciamento de sessão para proteção dos dados e acesso.
*   **Análise de Dados Detalhada:** Visualização e filtragem de dados operacionais, acompanhamento de desempenho e tendências.

## 🎯 Objetivos do Projeto

Este projeto final, desenvolvido no contexto da disciplina de Inteligência Artificial do UniSenac, teve como objetivos principais:

*   Aplicar técnicas de IA para resolver problemas empresariais reais no setor de logística.
*   Desenvolver uma interface funcional e amigável que exponha as soluções de IA de forma eficaz.
*   Integrar modelos de IA de forma coesa com um front-end utilizável.
*   Aproveitar e consolidar conhecimentos adquiridos em diversas disciplinas do curso.
*   Criar uma solução que demonstre valor real e tangível para o negócio de transportadoras.
*   Demonstrar a viabilidade técnica e comercial da aplicação de IA em gestão logística.

## 👥 Autores

*   **Fábio Briddi** - Desenvolvimento e Conceito
*   **Gustavo Casarin** - Desenvolvimento e Documentação

## 🚀 Funcionalidades Principais

O SisLog oferece um conjunto abrangente de funcionalidades projetadas para otimizar a gestão logística:

### 🔒 Sistema de Autenticação e Segurança

*   **Autenticação Segura:** Tela de login robusta que valida usuários contra um banco de dados, garantindo acesso autorizado.
*   **Gerenciamento de Sessão:** Proteção de acesso às páginas internas, exigindo login para navegação e operações, assegurando a integridade dos dados.

### 📊 Visualização e Análise de Dados Operacionais

*   **Navegação e Filtragem de Dados (Browse):**
    *   Telas dedicadas para visualização detalhada de dados operacionais, incluindo **Clientes**, **Veículos**, **Rotas**, **Entregas** e **Coletas**.
    *   Implementação de um sistema de filtro dinâmico para facilitar a localização e análise de informações específicas.
*   **Análise de Clientes com Machine Learning:**
    *   Utilização do algoritmo **K-Means Clustering** para classificar clientes com base em padrões de dados (e.g., volume de pedidos, frequência, tipo de mercadoria).
    *   Geração de **gráficos intuitivos** que visualizam os clusters de clientes, permitindo identificar perfis e estratégias de atendimento personalizadas.
*   **Análise de Entregas e Desempenho de Veículos:**
    *   Criação de gráficos de **comparação anual** e **evolução mensal** do volume de entregas, oferecendo insights sobre o crescimento e sazonalidade das operações.
    *   Aplicação de **Regressão Linear** para prever tendências de desempenho para diferentes tipos de veículos (e.g., consumo de combustível, tempo de entrega, capacidade de carga), auxiliando na gestão da frota e na manutenção preditiva.

### 🗺️ Otimização de Rotas de Coletas

*   **Seleção Interativa de Coletas:** Uma interface intuitiva permite a seleção de múltiplos pontos de coleta em um mapa ou lista.
*   **Cálculo de Rota Eficiente com Google Maps API:**
    *   Integração direta com a **Google Maps Directions API** para calcular a rota mais eficiente (considerando distância, tempo e tráfego) entre um ponto de partida definido, os pontos de coleta selecionados e um destino final.
    *   Gerenciamento inteligente de permissões de usuário para alternar entre o uso da API paga (para otimização de rotas em tempo real com acesso a recursos avançados) e uma API simulada/gratuita (para desenvolvimento e demonstração sem custos).
    *   Exibição clara e organizada do roteiro otimizado em formato de tabela.
    *   Opção para visualizar a rota otimizada diretamente no Google Maps, facilitando a navegação e o acompanhamento.

## 💻 Tecnologias Utilizadas

Este projeto foi construído utilizando uma stack tecnológica robusta e moderna, com foco em Python para o backend e Machine Learning, e padrões web para o frontend:

*   **Backend:**
    *   **Python**: A linguagem de programação principal, escolhida por sua versatilidade, vasta gama de bibliotecas e forte comunidade, ideal para desenvolvimento web e IA.
    *   **Flask**: Um microframework web leve e flexível para Python, utilizado para construir a aplicação web, gerenciar rotas, requisições HTTP e renderização de templates.
    *   **SQLAlchemy**: (Sugestão: Se você usa um ORM para o banco de dados, mencione-o aqui. Caso contrário, ignore ou mencione a biblioteca de conexão SQL que usa) - Para ORM e gerenciamento de banco de dados.
    *   **Python-dotenv**: Essencial para gerenciar variáveis de ambiente e chaves secretas de forma segura e prática (como a chave da API do Google Maps), garantindo que informações sensíveis não sejam expostas no código-fonte.
*   **Análise de Dados e Machine Learning:**
    *   **Pandas**: A biblioteca padrão em Python para manipulação e análise de dados, fundamental para processar e estruturar os grandes volumes de dados operacionais da transportadora.
    *   **Scikit-learn**: A biblioteca líder para Machine Learning em Python, utilizada para implementar algoritmos como **K-Means Clustering** (para classificação de clientes) e **Linear Regression** (para previsão de desempenho).
*   **Visualização de Dados:**
    *   **Matplotlib**: Uma biblioteca completa para criação de gráficos estáticos, animadas e interativas, utilizada para gerar as visualizações das análises de clientes e entregas.
    *   **Seaborn**: Construída sobre o Matplotlib, oferece uma interface de alto nível para criar gráficos estatísticos mais atraentes e informativos, facilitando a compreensão dos insights gerados.
*   **Frontend:**
    *   **HTML5**: A linguagem de marcação padrão para estruturar o conteúdo das páginas web.
    *   **CSS3**: Utilizado para estilizar as páginas, garantindo uma interface visualmente agradável e responsiva.
    *   **JavaScript**: Para adicionar interatividade dinâmica ao frontend, como a manipulação de mapas e formulários.
*   **Otimização de Rotas:**
    *   **Google Maps Directions API**: A API da Google utilizada para o cálculo e otimização de rotas de coletas, fornecendo dados precisos de geolocalização e direções.
*   **Outras Bibliotecas (identificadas na análise do `t.txt`):**
    *   **NumPy**: Biblioteca fundamental para computação numérica de alto desempenho, subjacente a Pandas e Scikit-learn.
    *   **requests**: Para realizar requisições HTTP, essencial para interagir com APIs externas como a do Google Maps.
    *   **Pillow**: (ou PIL) Utilizada para manipulação de imagens, podendo ser útil para lidar com avatares de usuário, logotipos ou outros elementos visuais.
    *   **Flask-related**: `itsdangerous`, `werkzeug` (componentes internos do Flask).
    *   **Date/Time Handling**: `python-dateutil`, `pytz`, `tzdata` (para manipulação robusta de datas e fusos horários).

## ⚙️ Como Executar o Projeto

Siga os passos abaixo para configurar e executar o SisLog em seu ambiente local:

### 1. Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes softwares instalados em sua máquina:

*   **Python**: Versão 3.8 ou superior. Você pode verificar sua versão digitando `python --version` (ou `python3 --version`) no terminal. Se precisar instalar, visite o site oficial do Python: [python.org](https://www.python.org/downloads/).
*   **Git**: Para clonar o repositório do projeto. Verifique sua instalação com `git --version`. Se não tiver, faça o download em: [git-scm.com](https://git-scm.com/downloads).

### 2. Configuração do Ambiente

Esta etapa envolve a obtenção do código, a criação de um ambiente isolado para o projeto e a instalação de todas as dependências necessárias.

*   **2.1. Clone o repositório (ou use sua pasta local):**

    Abra seu terminal ou prompt de comando e navegue até o diretório onde você deseja salvar o projeto. Em seguida, execute os comandos abaixo para clonar o repositório e entrar na pasta do projeto:

    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```
    > **Observação:** Lembre-se de substituir `https://github.com/seu-usuario/seu-repositorio.git` pelo link real do seu repositório Git.

*   **2.2. Crie e ative um ambiente virtual:**

    É altamente recomendado usar um ambiente virtual para isolar as dependências deste projeto do ambiente global do seu Python, evitando conflitos com outros projetos.

    *   **No Windows:**

        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

    *   **No macOS/Linux:**

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    > Após a ativação, você verá `(venv)` no início da linha de comando do seu terminal, indicando que o ambiente virtual está ativo.

*   **2.3. Instale as dependências:**

    Com o ambiente virtual ativado, instale todas as bibliotecas Python necessárias para o projeto. Elas estão listadas no arquivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```
    > Este comando pode levar alguns minutos, dependendo da sua conexão com a internet e do número de dependências.

*   **2.4. Configure a Chave da API do Google Maps (Opcional):**

    Para utilizar a funcionalidade de otimização de rotas com a API real do Google Maps, você precisará de uma chave de API válida. Se você não tiver uma ou preferir usar a API simulada, pode pular esta etapa por enquanto.

    1.  **Crie um arquivo `.env`:**
        Na **pasta raiz do projeto** (o mesmo diretório onde você encontra o `app.py`, `requirements.txt`, etc.), crie um novo arquivo de texto e salve-o com o nome `.env`.

    2.  **Adicione sua chave de API:**
        Abra o arquivo `.env` recém-criado com um editor de texto e adicione a seguinte linha, substituindo `"SUA_CHAVE_DE_API_REAL_VAI_AQUI"` pela sua chave real da API do Google Maps:

        ```
        GOOGLE_MAPS_API_KEY="SUA_CHAVE_DE_API_REAL_VAI_AQUI"
        ```

    > **Observação de Segurança:** O arquivo `.env` está listado no `.gitignore` do projeto. Isso significa que sua chave secreta **NUNCA será enviada para o repositório público**, garantindo a segurança de suas credenciais.

*   **2.5. Configuração da Estrutura de Dados:**

    O projeto espera que os arquivos de dados (.csv) utilizados para as análises e modelos de IA estejam em um local específico dentro da estrutura do projeto.

    *   Certifique-se de que a pasta `DataSets` (localizada na raiz do seu projeto, ao lado de `app.py`, `modules`, `static`, etc.) exista e contenha todos os arquivos `.csv` necessários para as análises e modelos de IA.
    *   Caso a localização da pasta `DataSets` ou dos arquivos `.csv` seja diferente da estrutura padrão do projeto, você precisará **ajustar os caminhos** referenciados no seu código-fonte (provavelmente em `app.py` ou nos módulos de análise dentro da pasta `modules`).

    *Exemplo da estrutura de dados esperada na raiz do projeto:*
    ```
    STRANS-Projeto-IA/
    ├── app.py
    ├── DataSets/                # Esta é a pasta esperada
    │   ├── clientes.csv
    │   ├── entregas.csv
    │   └── veiculos.csv
    ├── ... (outras pastas e arquivos)
    ```

### 3. Execução do Projeto

Com todas as configurações feitas e o ambiente virtual ativado, você está pronto para iniciar a aplicação web do SisLog.

*   **3.1. Inicie a aplicação web do SisLog:**

    No terminal, ainda dentro da pasta raiz do projeto e com o ambiente virtual ativado, execute o seguinte comando para iniciar o **servidor de desenvolvimento** que hospeda o seu SisLog:

    ```bash
    flask run
    ```
    > Você verá mensagens no terminal indicando que o servidor foi iniciado e o endereço em que ele está rodando. Isso significa que sua aplicação web (o site do SisLog) está agora "no ar" localmente e pronta para ser acessada.

*   **3.2. Acesse a aplicação no navegador:**

    Abra seu navegador web (Google Chrome, Firefox, Edge, etc.) e acesse o endereço fornecido pelo Flask. Geralmente, será:

    ```
    http://127.0.0.1:5000
    ```
    > Este é o endereço local padrão para aplicações Flask.

*   **3.3. Credenciais de Login (para Teste):**

    Ao acessar a aplicação, você será direcionado para a tela de login. Use as seguintes credenciais para fazer login e explorar o sistema:

    *   **Login:** `admin`
    *   **Senha:** `q1w2e3r4`
## 📂 Estrutura do Projeto

A seguir, uma visão geral da estrutura de pastas e arquivos principais do projeto:

. ├── .vscode/ # Configurações do VS Code ├── datasets/ # Contém os arquivos de dados (.csv) para análise e treinamento ├── modules/ # Módulos Python personalizados do projeto (lógica de negócio, IA) │ └── pycache/ ├── static/ # Arquivos estáticos da aplicação web (CSS, JS, Imagens) │ ├── analise/ # Possíveis arquivos de análise estática ou relatórios │ ├── css/ # Folhas de estilo CSS │ └── images/ # Imagens utilizadas na interface ├── STRANS_Projeto_IA/ # Diretório principal da aplicação Flask (código-fonte da aplicação) ├── templates/ # Arquivos HTML para renderização das páginas web ├── venv/ # Ambiente virtual Python │ ├── Include/ │ ├── Lib/ │ └── Scripts/ ├── .env.example # Exemplo de arquivo .env para configuração de variáveis de ambiente ├── .gitignore # Arquivos e pastas a serem ignorados pelo Git ├── app.py # (ou outro arquivo principal do Flask) - Ponto de entrada da aplicação ├── requirements.txt # Lista de dependências Python do projeto └── README.md # Este arquivo

## 📈 Melhorias Futuras (Roadmap)

Este projeto está em constante evolução. Algumas ideias para futuras melhorias incluem:

*   Implementação de um sistema de agendamento de entregas.
*   Integração com APIs de terceiros para informações de tráfego em tempo real mais precisas.
*   Desenvolvimento de um painel de controle (dashboard) mais interativo para monitoramento em tempo real.
*   Expansão dos modelos de IA para incluir previsão de demanda ou manutenção preditiva de veículos.
*   Melhorias na interface do usuário (UI) e experiência do usuário (UX).

## 🤝 Contribuição

Contribuições são bem-vindas! Se você tiver sugestões, relatórios de bugs ou quiser contribuir com código, por favor:

1.  Faça um `fork` do repositório.
2.  Crie uma nova `branch` para sua funcionalidade ou correção (`git checkout -b feature/minha-nova-funcionalidade`).
3.  Faça suas alterações e `commit` (`git commit -m 'feat: Adiciona nova funcionalidade X'`).
4.  Envie suas alterações (`git push origin feature/minha-nova-funcionalidade`).
5.  Abra um `Pull Request` detalhando suas mudanças.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) (crie este arquivo se ainda não existir) para mais detalhes.

## 📧 Contato

Para dúvidas, sugestões ou suporte, entre em contato com os autores:

*   **Fábio Briddi:** [fbriddi@gmail.com.br]
*   **Gustavo Casarin:** [gustavocasarinsilva@gmail.com]
