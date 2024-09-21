import requests
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

AIR_QUALITY_API_KEY = os.getenv('e5cf8ba5f1aaf90b90f7112023f47128')

def get_air_quality(lat, lng):
    response = requests.get(f'http://api.airqualityapi.com/v1/current?lat={lat}&lng={lng}&key={AIR_QUALITY_API_KEY}', verify = certifi.where())
    data = response.json()
    return data
