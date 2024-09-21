import requests
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

GEOCODING_API_KEY = os.getenv('AIzaSyDP7b0pFz-yQP2aRq-AGPm2EXvjHpFruR8')

def geocode_address(address):
    api_key=os.getenv("GEOCODING_API_KEY")
    response = requests.get(f'http://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}', verify = certifi.where())
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        raise Exception("Geocoding API error")
