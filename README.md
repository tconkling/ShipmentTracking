### Installation

```bash
$ pipenv install
```

### Running

```bash
$ pipenv shell
$ python main.py
```

This will start a web server on port 5001

### Usage

Call the "get_shipment_data" endpoint: 
http://127.0.0.1:5001/get_shipment_data?shipmentId=771298756318

This will:
- Populate a local sqlite database ("database.db") with shipment information from Fedex and sensor data from onasset
- Immediately read that data back out of the database and return it as a JSON blob