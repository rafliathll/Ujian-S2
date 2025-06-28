

import flask
from flask import Flask, jsonify, request
import time
import random

app = Flask(__name__)

mock_product_stock = {
    "SKU-001": {"name": "Wireless Mouse Pro", "stock": 150, "warehouse": "Gudang A"},
    "SKU-002": {"name": "Mechanical Keyboard RGB", "stock": 0, "warehouse": "Gudang B"},
    "SKU-003": {"name": "4K Webcam", "stock": 75, "warehouse": "Gudang A"},
    "SKU-004": {"name": "USB-C Hub 8-in-1", "stock": 210, "warehouse": "Gudang C"},
    "SKU-005": {"name": "Gaming Headset 7.1", "stock": 45, "warehouse": "Gudang B"},
}
valid_skus = list(mock_product_stock.keys())

@app.route('/get_stock', methods=['GET'])
def get_stock():
    sku_param = request.args.get('sku')
    delay = random.uniform(0.2, 0.6)
    time.sleep(delay)
    if sku_param:
        sku = sku_param.upper()
        if sku in mock_product_stock:
            data = mock_product_stock[sku]
            data["sku"] = sku
            print(f"[SERVER] Sending stock for {sku}: {data} (after {delay:.2f}s delay)")
            return jsonify(data)
        else:
            error_msg = {"error": "sku_not_found", "message": f"Product with SKU '{sku}' not found in inventory."}
            print(f"[SERVER] SKU {sku} not found (after {delay:.2f}s delay)")
            return jsonify(error_msg), 404
    else:
        error_msg = {"error": "bad_request", "message": "Parameter 'sku' is required."}
        return jsonify(error_msg), 400

if __name__ == '__main__':
    print("Simple E-commerce Stock API Server running on http://127.0.0.1:5000")
    print("Endpoint: GET /get_stock?sku=SKU-001")
    app.run(debug=False, threaded=True, use_reloader=False)