from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

class AddressRequest(BaseModel):
    address: str

@app.post("/analyze-route")
def analyze_route(req: AddressRequest):
    # Wymuszenie kontekstu Warszawy dla większej precyzji
    search_query = f"{req.address}, Warszawa"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={search_query}&key={API_KEY}&language=pl"

    response = requests.get(url).json()

    if response['status'] != 'OK' or not response['results']:
    # Zamiast domyślnego "Nie rozpoznano", zwróćmy powód błędu
     return {"district": f"Błąd API: {response['status']}"}

    components = response['results'][0]['address_components']
    district = "Brak danych"
    neighborhood = ""

    for comp in components:
        if 'sublocality_level_1' in comp['types']:
            district = comp['long_name']
        if 'neighborhood' in comp['types']:
            neighborhood = comp['long_name']

    result = f"{district} ({neighborhood})" if neighborhood else district
    return {"district": result}

# AIzaSyAm5irPvvFgTDv_FuXpLTZHWg8rKu4IFw8