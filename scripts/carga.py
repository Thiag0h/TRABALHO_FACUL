import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

MEU_HOST = os.getenv('DB_HOST')
MEU_PORT = os.getenv('DB_PORT')
MEU_BANCO = os.getenv('DB_NAME')
MEU_USUARIO = os.getenv('DB_USER')
MINHA_SENHA = os.getenv('DB_PASSWORD')

def carregar_postgres(arquivo_parquet):

    caminho_s3 = arquivo_parquet
    
    print(f"A ler o ficheiro do S3: {caminho_s3}")
    
    # Ler o arquivo Parquet do S3
    df = pd.read_parquet(caminho_s3)
    
    # Credenciais do banco PostgreSQL 18
    db_user = 'postgres' 
    db_pass = '982305395'
    db_host = 'host.docker.internal' 
    db_port = '5432'
    db_name = 'clima' 
    
    # Criar a conexão com o banco
    string_conexao = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(string_conexao)
    
    nome_tabela = 'dados_climaticos'
    
    print(f"A inserir dados na tabela '{nome_tabela}'...")
    
    # Inserir no PostgreSQL
    df.to_sql(nome_tabela, engine, if_exists='append', index=False)
    
    print("Carga concluída com sucesso no PostgreSQL!")