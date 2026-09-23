import json
import boto3
from datetime import datetime
import requests
from config.config import OPEN_METEO_URL, LATITUDE, LONGITUDE, TIMEZONE, WEATHER_VARIABLES

def coletar_dados():
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": WEATHER_VARIABLES,
        "timezone": TIMEZONE,
        "forecast_days": 1
    }
    
    print("Consultando Open-Meteo...")
    response = requests.get(OPEN_METEO_URL, params=params, timeout=30)
    response.raise_for_status()
    dados = response.json()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"raw/clima_{timestamp}.json"
    
    # Conectar ao S3 e enviar o JSON
    s3_client = boto3.client('s3')
    bucket = "monitoramento-climatico-faculdade"
    
    s3_client.put_object(
        Bucket=bucket,
        Key=nome_arquivo,
        Body=json.dumps(dados, ensure_ascii=False, indent=4)
    )
    
    caminho_s3 = f"s3://{bucket}/{nome_arquivo}"
    print(f"Dados salvos no S3: {caminho_s3}")
    
    return caminho_s3

if __name__ == "__main__":
    coletar_dados()