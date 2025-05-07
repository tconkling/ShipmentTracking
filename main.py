import json
from typing import Any

import requests

FEDEX_TRACKING_URL = "https://apis.fedex.com/track/v1/trackingnumbers"
FEDEX_TRACKING_NUMBER = "771298756318"

FEDEX_TOKEN_URL = "https://apis.fedex.com/oauth/token"
FEDEX_CLIENT_ID = "l7d63c7891050f4a5782aee9775f916f53"
FEDEX_CLIENT_SECRET = "3a7adcf8253545d887571456559b49b7"


def get_fedex_bearer_token(client_id: str, client_secret: str) -> str:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(FEDEX_TOKEN_URL, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]


def get_fedex_tracking_data(tracking_number: str, bearer_token: str) -> Any:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    payload = {
        "includeDetailedScans": True,
        "trackingInfo": [
            {
                "trackingNumberInfo": {
                    "trackingNumber": tracking_number
                }
            }
        ]
    }

    response = requests.post(FEDEX_TRACKING_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()


def main() -> None:
    bearer_token = get_fedex_bearer_token(FEDEX_CLIENT_ID, FEDEX_CLIENT_SECRET)
    tracking_data = get_fedex_tracking_data(tracking_number=FEDEX_TRACKING_NUMBER, bearer_token=bearer_token)
    print(json.dumps(tracking_data, indent=2))



if __name__ == "__main__":
    main()
