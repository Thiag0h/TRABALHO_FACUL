from pathlib import Path


# Caminho raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


# Pastas de dados
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


# Criar as pastas automaticamente
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# Open-Meteo
LATITUDE = -22.9068
LONGITUDE = -43.1729

TIMEZONE = "America/Sao_Paulo"

WEATHER_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m"
]


# API
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"