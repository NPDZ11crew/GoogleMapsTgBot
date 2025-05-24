import json

import requests
import os


async def getDetails(id: str):
    url = os.getenv("baseUri") + "SearchPlaceDetailsById"
    params = {"id": id}

    try:
        response = requests.post(url, params=params, headers={"Accept": "application/json"}, verify=False)
        text = response.text
        data = json.loads(text)
        return data

    except Exception as e:
        text = f"Error: {str(e)}"
        return text
