import json
from typing import Any

import requests

from app import db

FEDEX_TRACKING_URL = "https://apis.fedex.com/track/v1/trackingnumbers"

FEDEX_TOKEN_URL = "https://apis.fedex.com/oauth/token"
FEDEX_CLIENT_ID = "l7d63c7891050f4a5782aee9775f916f53"
FEDEX_CLIENT_SECRET = "3a7adcf8253545d887571456559b49b7"

def _get_fedex_bearer_token(client_id: str, client_secret: str) -> str:
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


def _get_fedex_tracking_data(tracking_number: str, bearer_token: str) -> Any:
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

def _extract_fedex_address(data_json: Any) -> str:
    try:
        return f"{data_json["city"]}, {data_json["stateOrProvinceCode"]} ({data_json["countryCode"]})"
    except KeyError:
        return "UNKNOWN"

def _extract_fedex_scan_event(data_json: Any) -> Any:
    return {
        "timestamp": data_json["date"],
        "location": _extract_fedex_address(data_json["scanLocation"])
    }

def create_shipment_record(tracking_number: str) -> db.Shipment:
    """Query the Fedex tracking endpoint and return a db.Shipment record for the given tracking number"""
    bearer_token = _get_fedex_bearer_token(FEDEX_CLIENT_ID, FEDEX_CLIENT_SECRET)
    tracking_data = _get_fedex_tracking_data(tracking_number=tracking_number, bearer_token=bearer_token)

    track_results = tracking_data["output"]["completeTrackResults"][0]["trackResults"][0]
    origin = track_results["shipperInformation"]["address"]
    destination = track_results["recipientInformation"]["address"]
    return db.Shipment(
        id=track_results["trackingNumberInfo"]["trackingNumber"],
        origin=_extract_fedex_address(origin),
        destination=_extract_fedex_address(destination),
        status=track_results["latestStatusDetail"]["description"],
    )
