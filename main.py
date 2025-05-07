from typing import Any

from flask import Flask, request, jsonify

from app import db, fedex, onasset

app = Flask(__name__)

def populate_db(shipment_id: str) -> None:
    """Populate the database with Shipment and SensorEvent data for the given shipment_id"""
    # Create/update the Shipment row:
    with db.Session() as session:
        try:
            shipment_data = fedex.create_shipment_record(shipment_id)
            session.merge(shipment_data)
            session.commit()
            print(f"Added Shipment (id={shipment_data.id})")
        except:
            print("Failed to add Shipment")
            session.rollback()
            raise

    # Create/update SensorEvent rows:
    with db.Session() as session:
        try:
            sensor_event_rows = onasset.create_sensorevent_records(shipment_id)
            for sensor_event in sensor_event_rows:
                session.merge(sensor_event)
            session.commit()
            print(f"Added {len(sensor_event_rows)} SensorEvents")
        except:
            print("Failed to add SensorEvents")
            session.rollback()
            raise

def fetch_from_db(shipment_id: str) -> Any:
    """Return a JSON object with shipment and sensor data for the given shipment_id.
    The database must have been populated with the data already.
    """
    with db.Session() as session:
        shipment = session.query(db.Shipment).filter(db.Shipment.id == shipment_id).first()
        sensor_events = session.query(db.SensorEvent).filter(db.SensorEvent.shipment_id == shipment_id)

        result = shipment.to_json()
        result["events"] = [event.to_json() for event in sensor_events]
        return result


@app.route('/')
def hello():
    return "Server is running!"


@app.route('/get_shipment_data', methods=['GET'])
def get_shipment_data():
    shipment_id = request.args.get('shipmentId', '')
    if len(shipment_id) == 0:
        return jsonify({"error": "bad shipmentID"}), 400

    # Populate the database with data about the given shipment...
    populate_db(shipment_id)

    # And then read that data right back out of the database!
    shipment_data = fetch_from_db(shipment_id)

    return jsonify(shipment_data)

def main() -> None:
    db.init_db()

    # Set debug=True during development for auto-reloading
    app.run(debug=True, host='0.0.0.0', port=5001)

if __name__ == "__main__":
    main()
