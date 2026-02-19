import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates')

# --- TEMPORARY DATABASE ---
# Stores the incoming webhooks temporarily in memory
recent_payments = {}

# --- SERVE THE FRONTEND ---
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# --- RECEIVE WEBHOOK FROM GATEWAY ---
@app.route('/webhook', methods=['POST'])
def mmpay_webhook():
    try:
        data = request.get_json()
        print(f"💰 WEBHOOK RECEIVED: {data}")

        if data and 'orderId' in data:
            # Save the payload using the orderId as the key
            recent_payments[data['orderId']] = data

        return jsonify({"status": "received"}), 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"status": "error"}), 500

# --- API FOR FRONTEND TO FETCH RECEIPT DATA ---
@app.route('/api/receipt/<order_id>', methods=['GET'])
def get_receipt(order_id):
    data = recent_payments.get(order_id)
    if data:
        return jsonify({"status": "found", "data": data}), 200
    else:
        return jsonify({"status": "pending"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)