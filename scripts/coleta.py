import json
import boto3
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime
from config.config import OPEN_METEO_URL, LATITUDE, LONGITUDE, TIMEZONE, WEATHER_VARIABLES

# Configurações de Sessão e Cache
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

class Coord:
    def __init__(self, zona, cidade, latitude, longitude):
        self.zona = zona
        self.cidade = cidade
        self.latitude = latitude
        self.longitude = longitude

def extração_coord(zona):
    latitude = [coordenadas.latitude for coordenadas in zona]
    longitude = [coordenadas.longitude for coordenadas in zona]
    return latitude, longitude

def montar_params(latitude, longitude):
    return {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_mean",
        "past_days": 30,
        "forecast_days": 0,
    }

def responses(param):
    return openmeteo.weather_api(OPEN_METEO_URL, params=param)

def get_results(zona, response_area):
    dataframes = []
    for coordenada, response in zip(zona, response_area):
        daily = response.Daily()
        daily_temperature_2m_mean = daily.Variables(0).ValuesAsNumpy()

        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            )
        }

        daily_data["temperature_2m"] = daily_temperature_2m_mean
        daily_data["zona"] = coordenada.zona
        daily_data["cidade"] = coordenada.cidade

        dataframes.append(pd.DataFrame(data=daily_data))
    return pd.concat(dataframes, ignore_index=True)

def coletar_dados():
    print("Consultando Open-Meteo para as diferentes zonas...")
    
    # Parametros Centro
    zcentro = [
        Coord("Zona Centro", "Centro", -22.90369, -43.18777),
        Coord("Zona Centro", "Gamboa", -22.89750, -43.19278),
    ]
    latCentro, longCentro = extração_coord(zcentro)
    paramCentro = montar_params(latCentro, longCentro)
    responsesCentro = responses(paramCentro)
    dadosCentro = get_results(zcentro, responsesCentro)

    # Parametros Zona Sul
    zsul = [Coord("Zona Sul", "Flamengo", -22.93560, -43.17680)]
    latSul, longSul = extração_coord(zsul)
    paramSul = montar_params(latSul, longSul)
    responsesSul = responses(paramSul)
    dadosSul = get_results(zsul, responsesSul)

    # Parametros Zona Norte
    znorte = [Coord("Zona Norte", "Maracana", -22.91180, -43.23200)]
    latNorte, longNorte = extração_coord(znorte)
    paramNorte = montar_params(latNorte, longNorte)
    responsesNorte = responses(paramNorte)
    dadosNorte = get_results(znorte, responsesNorte)

    # Parametros Zone Oeste
    zoeste = [Coord("Zona Oeste", "Barra da Tijuca", -23.00000, -43.36500)]
    latOeste, longOeste = extração_coord(zoeste)
    paramOeste = montar_params(latOeste, longOeste)
    responsesOeste = responses(paramOeste)
    dadosOeste = get_results(zoeste, responsesOeste)

    # Consolidação dos Dados
    dadosTotais = pd.concat([dadosCentro, dadosSul, dadosNorte, dadosOeste], ignore_index=True)

    # Converte o DataFrame formatado para uma string JSON baseada em registros
    dados_json_str = dadosTotais.to_json(orient="records", date_format="iso", force_ascii=False)
    
    # Para manter a endentação legível no arquivo do S3, carregamos e fazemos dump com identação
    dados_formatados = json.loads(dados_json_str)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"raw/clima_{timestamp}.json"
    bucket = "monitoramento-climatico-faculdade"
    
    # Conectar ao S3 e enviar o arquivo JSON
    s3_client = boto3.client('s3')
    
    s3_client.put_object(
        Bucket=bucket,
        Key=nome_arquivo,
        Body=json.dumps(dados_formatados, ensure_ascii=False, indent=4)
    )
    
    caminho_s3 = f"s3://{bucket}/{nome_arquivo}"
    print(f"Dados salvos no S3: {caminho_s3}")
    
    # ALTERAÇÃO AQUI: Retorna apenas a chave (nome_arquivo) para o XCom passar para a transformação
    return nome_arquivo

if __name__ == "__main__":
    coletar_dados()