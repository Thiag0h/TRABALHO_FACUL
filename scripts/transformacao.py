import pandas as pd
import boto3
from io import StringIO
import os

def calcular_operacoes_zona(dados_zona, operacao, freq=None):
    if freq is None:
        return dados_zona["temperature_2m"].agg(operacao)
    else:
        return dados_zona.groupby(pd.Grouper(key="date", freq=freq))["temperature_2m"].agg(operacao)

def carregar_dados_s3(bucket, key):
    """Lê o arquivo JSON do S3 e converte de volta para DataFrame"""
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key=key)
    
    dados_json = response['Body'].read().decode('utf-8')
    df = pd.read_json(StringIO(dados_json), orient='records')
    
    # Garante que a coluna date seja interpretada como data/hora pelo Pandas
    df['date'] = pd.to_datetime(df['date'])
    return df

def executar_calculos(nome_arquivo_s3):
    bucket = "monitoramento-climatico-faculdade"
    
    print(f"Lendo arquivo {nome_arquivo_s3} do S3...")
    dadosTotais = carregar_dados_s3(bucket, nome_arquivo_s3)

    # Separação por zonas
    dados_zona_centro = dadosTotais[dadosTotais["zona"] == "Zona Centro"]
    dados_zona_sul = dadosTotais[dadosTotais["zona"] == "Zona Sul"]
    dados_zona_norte = dadosTotais[dadosTotais["zona"] == "Zona Norte"]
    dados_zona_oeste = dadosTotais[dadosTotais["zona"] == "Zona Oeste"]

    print("\n--- Média Diária: Zona Centro ---")
    media_centro = calcular_operacoes_zona(dados_zona_centro, operacao='mean', freq='D')
    print(media_centro.head())

    print("\n--- Temperatura Máxima Diária: Zona Norte ---")
    max_norte = calcular_operacoes_zona(dados_zona_norte, operacao='max', freq='D')
    print(max_norte.head())
    
    print("\n--- Temperatura Mínima Geral: Zona Sul ---")
    min_sul_geral = calcular_operacoes_zona(dados_zona_sul, operacao='min')
    print(f"Mínima absoluta na Zona Sul: {min_sul_geral}")

    # 1. Juntar os dados consolidados (ajuste conforme a regra de negócio desejada)
    df_final = pd.concat([dados_zona_centro, dados_zona_sul, dados_zona_norte, dados_zona_oeste])

    # 2. Salvar como Parquet temporariamente e enviar para o S3
    arquivo_parquet_local = "/tmp/dados_transformados.parquet"
    df_final.to_parquet(arquivo_parquet_local, index=False)

    # Extraindo o timestamp do nome original para criar um nome de arquivo rastreável
    # Exemplo: de "raw/clima_20260924_185000.json" para "arquivo_20260924_185000.parquet"
    nome_base = nome_arquivo_s3.split('/')[-1].replace('.json', '')
    caminho_s3_processed = f"processed/dados_clima.parquet"
    
    s3_client = boto3.client('s3')
    s3_client.upload_file(arquivo_parquet_local, bucket, caminho_s3_processed)
    
    caminho_completo_s3 = f"s3://{bucket}/{caminho_s3_processed}"
    print(f"Dados transformados salvos no S3: {caminho_completo_s3}")
    
    # 3. Retornar o caminho para o XCom passar para a Carga
    return caminho_completo_s3

if __name__ == "__main__":
    # Apenas para testes manuais via terminal
    executar_calculos("raw/clima_teste.json")