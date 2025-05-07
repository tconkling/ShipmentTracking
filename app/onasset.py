from typing import Any, List

import requests

from app import config
from app import db
from app import util

ONASSET_URL = "https://oainsightapi.onasset.com/rest/2/sentry500s/864499064808214/reports"

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
    onasset_data = _get_onasset_data(config.ONASSET_TOKEN)

    return [db.SensorEvent(
        shipment_id=shipment_id,
        latitude=event_data["latitude"],
        longitude=event_data["longitude"],
        timestamp=util.str_to_datetime(event_data["timeOfReport"]),
        temp=event_data["temperatureC"]
    ) for event_data in onasset_data]