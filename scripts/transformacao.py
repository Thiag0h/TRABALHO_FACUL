import json
import pandas as pd
import s3fs

def transformar_dados(arquivo_json):
    print(f"Iniciando transformação de: {arquivo_json}")

    # Ler JSON diretamente do S3
    fs = s3fs.S3FileSystem()
    with fs.open(arquivo_json, "rb") as f:
        dados = json.load(f)

    hourly = dados.get("hourly", {})

    df = pd.DataFrame({
        "data_hora": hourly.get("time", []),
        "temperatura": hourly.get("temperature_2m", []),
        "umidade": hourly.get("relative_humidity_2m", []),
        "precipitacao": hourly.get("precipitation", []),
        "velocidade_vento": hourly.get("wind_speed_10m", [])
    })

    if df.empty:
        raise ValueError("O JSON não continha dados válidos.")

    df["data_hora"] = pd.to_datetime(df["data_hora"])
    df = df.drop_duplicates()

    colunas_numericas = ["temperatura", "umidade", "precipitacao", "velocidade_vento"]
    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    df = df.dropna(subset=["temperatura"])

    df["data"] = df["data_hora"].dt.date
    df["hora"] = df["data_hora"].dt.hour

    if not df["umidade"].dropna().between(0, 100).all():
        raise ValueError("Valores de umidade fora de 0-100.")

    # Gerar nome dinâmico e salvar Parquet de volta no S3
    nome_base = arquivo_json.split('/')[-1].replace('.json', '')
    bucket = "monitoramento-climatico-faculdade"
    arquivo_saida = f"s3://{bucket}/processed/clima_processado.parquet"

    # Salva no S3 (o pandas usa o s3fs por baixo dos panos)
    df.to_parquet(arquivo_saida, index=False)
    print(f"Dados transformados salvos no S3: {arquivo_saida}")
    
    return arquivo_saida