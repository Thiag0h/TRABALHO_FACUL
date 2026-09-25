import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

TABELAS_POSTGRES = {
    "mensal": "dados_mensais",
    "semanal": "dados_semanais",
    "diario": "dados_diarios",
}

def carregar_postgres(caminhos_s3):
    string_conexao = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(string_conexao)

    for chave, caminho_s3 in caminhos_s3.items():
        nome_tabela = TABELAS_POSTGRES[chave]
        print(f"Lendo {caminho_s3}...")
        df = pd.read_parquet(caminho_s3)

        print(f"Inserindo dados na tabela '{nome_tabela}'...")
        df.to_sql(nome_tabela, engine, if_exists='replace', index=False)

    print("Carga concluÃda com sucesso no PostgreSQL!")