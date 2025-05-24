import os
import json
import requests


async def SearchByTextAsync(textQuery: str):
    url = os.getenv("baseUri") + "SearchText"
    params = {"searchText": textQuery}

    try:
        response = requests.post(url, params=params, headers={"Accept": "application/json"}, verify=False)
        text = response.text
        data = json.loads(text)

        return data
    except Exception as e:
        text = f"Error: {str(e)}"
        return text
