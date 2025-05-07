from typing import Any, List

import requests

from app import db
from app import util

ONASSET_URL = "https://oainsightapi.onasset.com/rest/2/sentry500s/864499064808214/reports"
ONASSET_TOKEN = "imc9tvgvmtShp-tPYqoHYhhseMWi_TNNTn1etxJ2WIGxn2GHSN51UUTjyz4pm0vnjnZp95-xSPJ2GBN6ccN1bACUipKpLs7wb3bYyxqXU1BtgTFBT1B-nCa3eNsVDvmva97PBi69s95lrxb-teffh4FKoMGlky3ehTL3iFtiJwZVnZWXEBgZG1MlWPCxjfKtqS7l4ab-mfbdJ5Cda6eO20SGV7e6-WxrjWlRdnuqlwmuvK74fCWyXHRTOBLNwXVVgGCd3GH9ZsevEskKMP-_hvMDqE_wVpUzBEOYO7dY5thCzf49kk-h2g8Hf3Kkn9V-VapcLBxh6oBLInQh9pflRKn2W56pZBwQ_yhegrIeNnc9fg7m7RaAXSFYZiHFCiCFDieisz4-XW9qctaC88C2mw"

def _get_onasset_data(bearer_token: str) -> Any:
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

def create_sensorevent_records(shipment_id: str) -> List[db.SensorEvent]:
    """Query the OnAsset tracking endpoint and return db.SensorEvent records for each sensor event for the
    given shipment_id."""
    onasset_data = _get_onasset_data(ONASSET_TOKEN)

    return [db.SensorEvent(
        shipment_id=shipment_id,
        latitude=event_data["latitude"],
        longitude=event_data["longitude"],
        timestamp=util.str_to_datetime(event_data["timeOfReport"]),
        temp=event_data["temperatureC"]
    ) for event_data in onasset_data]