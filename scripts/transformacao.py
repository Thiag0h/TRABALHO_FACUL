import pandas as pd
import boto3
from io import StringIO
import os

VARIAVEIS = {
    "temperatura": "temperature_2m",
    "umidade": "humidity_2m",
    "vento": "wind_speed_2m",
}

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

def _linha_estatisticas(grupo):
    linha = {}
    for nome, coluna in VARIAVEIS.items():
        linha[f"{nome}_media"] = grupo[coluna].mean()
        linha[f"{nome}_max"] = grupo[coluna].max()
        linha[f"{nome}_min"] = grupo[coluna].min()
    return linha

def montar_tabela_mensal(dadosTotais):
    linhas = []
    for zona, grupo in dadosTotais.groupby("zona"):
        linha = {"zona": zona}
        linha.update(_linha_estatisticas(grupo))
        linhas.append(linha)
    return pd.DataFrame(linhas)

def montar_tabela_semanal(dadosTotais):
    linhas = []
    for (semana, zona), grupo in dadosTotais.groupby([pd.Grouper(key="date", freq="W"), "zona"]):
        linha = {"semana": semana, "zona": zona}
        linha.update(_linha_estatisticas(grupo))
        linhas.append(linha)
    return pd.DataFrame(linhas)

def montar_tabela_diaria(dadosTotais):
    linhas = []
    for (dia, zona), grupo in dadosTotais.groupby([pd.Grouper(key="date", freq="D"), "zona"]):
        linha = {"dia": dia, "zona": zona}
        linha.update(_linha_estatisticas(grupo))
        linhas.append(linha)
    return pd.DataFrame(linhas)

def executar_calculos(nome_arquivo_s3):
    bucket = "monitoramento-climatico-faculdade"

    print(f"Lendo arquivo {nome_arquivo_s3} do S3...")
    dadosTotais = carregar_dados_s3(bucket, nome_arquivo_s3)

    df_mensal = montar_tabela_mensal(dadosTotais)
    df_semanal = montar_tabela_semanal(dadosTotais)
    df_diario = montar_tabela_diaria(dadosTotais)

    print("\n--- Tabela Mensal ---")
    print(df_mensal)
    print("\n--- Tabela Semanal (amostra) ---")
    print(df_semanal.head())
    print("\n--- Tabela Diária (amostra) ---")
    print(df_diario.head())

    caminhos = {}
    s3_client = boto3.client('s3')

    for nome_tabela, df in [("mensal", df_mensal), ("semanal", df_semanal), ("diario", df_diario)]:
        caminho_local = f"/tmp/dados_{nome_tabela}.parquet"
        df.to_parquet(caminho_local, index=False)

        caminho_s3 = f"processed/dados_{nome_tabela}.parquet"
        s3_client.upload_file(caminho_local, bucket, caminho_s3)
        caminhos[nome_tabela] = f"s3://{bucket}/{caminho_s3}"
        print(f"Tabela '{nome_tabela}' salva em: {caminhos[nome_tabela]}")

    return caminhos