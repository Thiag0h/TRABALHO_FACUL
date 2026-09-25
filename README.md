🌦️ Pipeline de Dados de Clima (Trabalho de Faculdade)

Este repositório contém um projeto de Engenharia de Dados desenvolvido como trabalho acadêmico. O projeto implementa um pipeline ETL (Extract, Transform, Load) completo para dados meteorológicos, orquestrado com Apache Airflow e conteinerizado via Docker.

🚀 Arquitetura e Tecnologias

O pipeline foi construído utilizando as seguintes tecnologias:

Python: Linguagem principal para os scripts de extração, transformação e carga.

Apache Airflow: Orquestração de tarefas (DAGs) e agendamento do pipeline.

Docker & Docker Compose: Gerenciamento do ambiente e infraestrutura local.

Parquet / JSON: Formatos de armazenamento de dados (Raw e Processed).

📂 Estrutura do Projeto

Abaixo está a organização dos diretórios e arquivos do projeto:

📦 TRABALHO_FACUL
 ┣ 📂 config/
 ┃ ┣ 📜 __init__.py
 ┃ ┗ 📜 config.py               # Configurações gerais (chaves de API, caminhos, etc)
 ┣ 📂 dags/
 ┃ ┗ 📜 clima_pipeline.py       # DAG do Airflow que orquestra o ETL
 ┣ 📂 data/
 ┃ ┣ 📂 processed/              # Dados limpos e transformados
 ┃ ┃ ┗ 📜 clima.parquet
 ┃ ┗ 📂 raw/                    # Dados brutos coletados da fonte
 ┃   ┗ 📜 clima_20260922_200249.json
 ┣ 📂 scripts/
 ┃ ┣ 📜 __init__.py
 ┃ ┣ 📜 coleta.py               # [Extract] Script de consumo da API de clima
 ┃ ┣ 📜 transformacao.py        # [Transform] Script de limpeza e conversão para Parquet
 ┃ ┗ 📜 carga.py                # [Load] Script para carregamento dos dados finais
 ┣ 📜 .gitignore                # Arquivos ignorados pelo Git
 ┗ 📜 docker-compose.yaml       # Configuração dos containers (Airflow, dependências)


⚙️ Fluxo do Pipeline (ETL)

Extração (scripts/coleta.py): Coleta dados meteorológicos (provavelmente via API externa) e armazena os resultados no formato bruto .json na pasta data/raw/.

Transformação (scripts/transformacao.py): Lê os dados brutos, realiza o tratamento, limpeza e tipagem, salvando o resultado no formato colunar .parquet na pasta data/processed/, otimizando a leitura.

Carga (scripts/carga.py): Prepara a disponibilização dos dados transformados para o destino final (banco de dados, data warehouse ou consumo analítico).

Orquestração (dags/clima_pipeline.py): O Airflow amarra todas essas etapas em uma DAG, garantindo que sejam executadas na ordem correta, registrando logs e lidando com eventuais falhas.

🛠️ Como executar o projeto localmente

Pré-requisitos:

Ter o Docker e o Docker Compose instalados na sua máquina.

Passo a passo:

Clone este repositório:

git clone <URL_DO_SEU_REPOSITORIO>
cd TRABALHO_FACUL


Inicie os containers do Docker:

docker-compose up -d


Acesse a interface web do Airflow:

Abra o navegador e acesse: http://localhost:8080 (ou a porta configurada no seu docker-compose.yaml).

Nota: Geralmente o usuário/senha padrão para o Airflow no Docker é airflow / airflow.

Na interface do Airflow, ative a DAG clima_pipeline e acione a execução (Trigger DAG) para acompanhar o fluxo dos dados.

📝 Autores

Thiago de Andrade Pena, Arthur de Souza Sá - Desenvolvimento do ETL e Arquitetura - Trabalho Acadêmico.
