from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Importação das funções corretas dos seus scripts
from scripts.coleta import coletar_dados 
from scripts.transformacao import executar_calculos
from scripts.carga import carregar_postgres # Importação da Carga adicionada

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 9, 24),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'clima_pipeline',
    default_args=default_args,
    description='Pipeline de ETL Completo: Coleta, Transformação e Carga',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    # TASK 1: EXTRAÇÃO
    task_coleta = PythonOperator(
        task_id='coletar_dados_api',
        python_callable=coletar_dados 
    )

    # TASK 2: TRANSFORMAÇÃO
    task_transformacao = PythonOperator(
        task_id='transformar_dados_s3',
        python_callable=executar_calculos,
        op_kwargs={'nome_arquivo_s3': '{{ ti.xcom_pull(task_ids="coletar_dados_api") }}'} 
    )

    # TASK 3: CARGA
    task_carga = PythonOperator(
        task_id='carregar_dados_postgres',
        python_callable=carregar_postgres,
        # O XCom vai pegar o caminho "s3://.../processed/arquivo.parquet" que a transformação devolveu
        op_kwargs={'arquivo_parquet': '{{ ti.xcom_pull(task_ids="transformar_dados_s3") }}'} 
    )

    # ORDEM DE EXECUÇÃO COMPLETA
    task_coleta >> task_transformacao >> task_carga