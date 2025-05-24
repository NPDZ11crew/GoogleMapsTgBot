import os
import json
import requests
import decimal


async def SearchNearbyByGeo(groupOfFacility: int, typesOfFacility: list[int],
                            lat: decimal = None, lng: decimal = None, rad: float = None,
                            city: str = None):
    decimal.getcontext().prec = 20
    url = os.getenv("baseUri") + "SearchText"
    params = {
        "groupOfFacility": groupOfFacility,
        "lat": lat,
        "lng": lng,
        "rad": rad
    }
    headers = {"Accept": "application/json"}

    try:
        response = requests.post(url, params=params, headers=headers, json=typesOfFacility, verify=False)
        text = response.text[:4096]
        data = json.loads(text)

        return data
    except Exception as e:
        text = f"Error: {str(e)}"
        return text
