import sys
# 1. Adicionar o diretório primeiro
sys.path.append('/opt/airflow')

# 2. Fazer as importações do Airflow e do Python
from airflow.decorators import dag, task
from datetime import datetime

# 3. Fazer as importações dos seus scripts
from scripts.coleta import coletar_dados
from scripts.transformacao import transformar_dados
from scripts.carga import carregar_postgres

@dag(
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["clima", "etl"]
)
def clima_pipeline():
    @task
    def extrair():
        return coletar_dados()

    @task
    def transformar(arquivo_json):
        return transformar_dados(arquivo_json)

    @task
    def carregar(arquivo_parquet):
        carregar_postgres(arquivo_parquet)

    # Fluxo de execução
    arquivo_json = extrair()
    arquivo_parquet = transformar(arquivo_json)
    carregar(arquivo_parquet)

# Inicializar a DAG
dag_instancia = clima_pipeline()