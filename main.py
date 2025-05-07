import json
from typing import Any

import requests
import streamlit as st

from app import db

FEDEX_TRACKING_URL = "https://apis.fedex.com/track/v1/trackingnumbers"
SHIPMENT_ID = "771298756318"

FEDEX_TOKEN_URL = "https://apis.fedex.com/oauth/token"
FEDEX_CLIENT_ID = "l7d63c7891050f4a5782aee9775f916f53"
FEDEX_CLIENT_SECRET = "3a7adcf8253545d887571456559b49b7"

ONASSET_URL = "https://oainsightapi.onasset.com/rest/2/sentry500s/864499064808214/reports"
ONASSET_TOKEN = "imc9tvgvmtShp-tPYqoHYhhseMWi_TNNTn1etxJ2WIGxn2GHSN51UUTjyz4pm0vnjnZp95-xSPJ2GBN6ccN1bACUipKpLs7wb3bYyxqXU1BtgTFBT1B-nCa3eNsVDvmva97PBi69s95lrxb-teffh4FKoMGlky3ehTL3iFtiJwZVnZWXEBgZG1MlWPCxjfKtqS7l4ab-mfbdJ5Cda6eO20SGV7e6-WxrjWlRdnuqlwmuvK74fCWyXHRTOBLNwXVVgGCd3GH9ZsevEskKMP-_hvMDqE_wVpUzBEOYO7dY5thCzf49kk-h2g8Hf3Kkn9V-VapcLBxh6oBLInQh9pflRKn2W56pZBwQ_yhegrIeNnc9fg7m7RaAXSFYZiHFCiCFDieisz4-XW9qctaC88C2mw"


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


def get_onasset_data(bearer_token: str) -> Any:
    params = {
        "from": "2025-01-08T15:46:00Z",
        "to": "2025-01-10T22:46:00Z"
    }

    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }

    response = requests.get(ONASSET_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def extract_fedex_address(data_json: Any) -> str:
    try:
        return f"{data_json["city"]}, {data_json["stateOrProvinceCode"]} ({data_json["countryCode"]})"
    except KeyError:
        return "UNKNOWN"

def extract_fedex_scan_event(data_json: Any) -> Any:
    return {
        "timestamp": data_json["date"],
        "location": extract_fedex_address(data_json["scanLocation"])
    }

def extract_fedex_shipment_data(data_json: Any) -> Any:
    track_results = data_json["output"]["completeTrackResults"][0]["trackResults"][0]
    origin = track_results["shipperInformation"]["address"]
    destination = track_results["recipientInformation"]["address"]
    return {
        "shipmentId": track_results["trackingNumberInfo"]["trackingNumber"],
        "origin": extract_fedex_address(origin),
        "destination": extract_fedex_address(destination),
        "status": track_results["latestStatusDetail"]["description"],
        "events": [extract_fedex_scan_event(event) for event in track_results["scanEvents"]]
    }

def extract_sensor_data(shipment_id: str, data_json: Any) -> Any:
    return [{
        "shipmentId": shipment_id,
        "latitude": event_data["latitude"],
        "longitude": event_data["longitude"],
        "timestamp": event_data["timeOfReport"],
        "temp": event_data["temperatureC"]
    } for event_data in data_json]

def main() -> None:
    bearer_token = get_fedex_bearer_token(FEDEX_CLIENT_ID, FEDEX_CLIENT_SECRET)
    tracking_data = get_fedex_tracking_data(tracking_number=SHIPMENT_ID, bearer_token=bearer_token)

    st.subheader("Extracted Tracking Data")
    st.json(extract_fedex_shipment_data(tracking_data))

    onasset_data = get_onasset_data(ONASSET_TOKEN)
    st.subheader("Extracted OnAsset data")
    st.json(extract_sensor_data(SHIPMENT_ID, onasset_data))

    db.init_db()



if __name__ == "__main__":
    main()
