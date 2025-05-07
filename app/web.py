from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/get_data', methods=['GET'])
def get_data():
    shipmentId = request.args.get('shipmentId', '')

    return jsonify({
    })

def init_web_app() -> None:
    # Set debug=True during development for auto-reloading
    app.run(debug=True, host='0.0.0.0', port=5000)