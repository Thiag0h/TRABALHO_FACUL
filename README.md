# 🌦️ Pipeline de Dados de Clima

Projeto acadêmico de **Engenharia de Dados** desenvolvido para implementar um pipeline ETL completo para dados meteorológicos.

O projeto realiza a **extração, transformação e carga de dados de clima**, utilizando Python, Apache Airflow e Docker. Os dados são inicialmente armazenados em formato bruto (`JSON`), tratados durante o processo de transformação e posteriormente disponibilizados em formato `Parquet` e no banco de dados para consumo analítico.

---

## 🚀 Arquitetura e Tecnologias

O pipeline utiliza as seguintes tecnologias:

* **Python** — desenvolvimento dos scripts de ETL.
* **Apache Airflow** — orquestração, agendamento e monitoramento do pipeline.
* **Docker / Docker Compose** — criação e gerenciamento do ambiente.
* **JSON** — armazenamento dos dados brutos.
* **Parquet** — armazenamento dos dados tratados.
* **Banco de Dados** — armazenamento e disponibilização dos dados para análise.
* **Power BI** — visualização e análise dos dados.

---

## 📂 Estrutura do Projeto

```text
TRABALHO_FACUL/
│
├── config/
│   ├── __init__.py
│   └── config.py
│
├── dags/
│   └── clima_pipeline.py
│
├── data/
│   ├── processed/
│   │   └── clima.parquet
│   │
│   └── raw/
│       └── clima_20260922_200249.json
│
├── scripts/
│   ├── __init__.py
│   ├── coleta.py
│   ├── transformacao.py
│   └── carga.py
│
├── .gitignore
└── docker-compose.yaml
```

### 📌 Principais arquivos

| Arquivo               | Descrição                                             |
| --------------------- | ----------------------------------------------------- |
| `coleta.py`           | Realiza a extração dos dados meteorológicos           |
| `transformacao.py`    | Realiza limpeza, tratamento e transformação dos dados |
| `carga.py`            | Carrega os dados tratados no destino final            |
| `clima_pipeline.py`   | DAG responsável pela orquestração do ETL              |
| `config.py`           | Centraliza configurações utilizadas pelo projeto      |
| `docker-compose.yaml` | Configura os containers e serviços do projeto         |

---

## ⚙️ Fluxo do Pipeline ETL

O pipeline é dividido em três etapas principais:

### 1. 🔎 Extract — Extração

O script `scripts/coleta.py` realiza a coleta dos dados meteorológicos a partir da fonte de dados configurada.

Os dados são armazenados inicialmente em formato **JSON**, preservando os dados brutos para posterior processamento.

```text
API de Clima
     │
     ▼
coleta.py
     │
     ▼
data/raw/*.json
```

### 2. 🔄 Transform — Transformação

O script `scripts/transformacao.py` lê os arquivos brutos e realiza as etapas de tratamento dos dados, como:

* Limpeza dos dados;
* Tratamento de valores;
* Conversão de tipos;
* Padronização das informações;
* Preparação dos dados para análise.

Após o processamento, os dados são armazenados em formato **Parquet**.

```text
data/raw/*.json
       │
       ▼
transformacao.py
       │
       ▼
data/processed/clima.parquet
```

### 3. 💾 Load — Carga

O script `scripts/carga.py` realiza o carregamento dos dados tratados para o destino final.

```text
clima.parquet
      │
      ▼
   carga.py
      │
      ▼
Banco de Dados
      │
      ▼
   Power BI
```

---

## 🔄 Orquestração com Apache Airflow

O Apache Airflow é responsável por orquestrar as etapas do pipeline através da DAG:

```text
clima_pipeline.py
```

A DAG organiza a execução das tarefas na sequência correta:

```text
Extract
  ↓
Transform
  ↓
Load
```

Além da execução das tarefas, o Airflow permite acompanhar:

* Status das tarefas;
* Logs de execução;
* Falhas;
* Tempo de execução;
* Histórico das execuções;
* Agendamento do pipeline.

---

## 🐳 Execução com Docker

### Pré-requisitos

Para executar o projeto localmente, é necessário possuir:

* Docker
* Docker Compose
* Git

### 1. Clone o repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd TRABALHO_FACUL
```

### 2. Inicie os containers

```bash
docker compose up -d
```

### 3. Acesse o Apache Airflow

Abra no navegador:

```text
http://localhost:8080
```

As credenciais dependem da configuração definida no `docker-compose.yaml`.

### 4. Execute a DAG

Na interface do Airflow:

1. Localize a DAG `clima_pipeline`;
2. Ative a DAG;
3. Clique em **Trigger DAG**;
4. Acompanhe a execução das tarefas;
5. Consulte os logs caso alguma etapa apresente erro.

---

## 📊 Consumo dos Dados

Após a execução do pipeline, os dados tratados podem ser utilizados para análise e visualização.

O **Power BI** pode ser conectado ao banco de dados para criação de dashboards e indicadores relacionados às condições meteorológicas.

Exemplos de análises:

* 🌡️ Temperatura média por dia;
* 📈 Variação da temperatura;
* 🌧️ Precipitação;
* 💨 Velocidade do vento;
* 📍 Comparação entre zonas/localidades;
* 📅 Médias móveis e análises temporais.

---

## 🎯 Objetivo do Projeto

O objetivo deste trabalho é demonstrar, de forma prática, conceitos fundamentais de **Engenharia de Dados**, incluindo:

* Extração de dados;
* Processamento e transformação;
* Armazenamento em diferentes formatos;
* Construção de pipeline ETL;
* Orquestração com Apache Airflow;
* Containerização com Docker;
* Integração com banco de dados;
* Disponibilização dos dados para ferramentas de BI.

---

## 👨‍💻 Autores

**Thiago de Andrade Pena**
**Arthur de Souza Sá**

Projeto desenvolvido como trabalho acadêmico.
