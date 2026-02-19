import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# This matches the endpoint in your callbackUrl: https://your-site.up.railway.app/webhook
@app.route('/webhook', methods=['POST'])
def mmpay_webhook():
    # 1. Get JSON data from the request
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "No data"}), 400

    # 2. Extract values sent by MMPay
    # Typical payload: {"orderId": "APK-12345", "status": "success", "amount": 5000}
    order_id = data.get('orderId')
    status = data.get('status')
    amount = data.get('amount')

    print(f"🔔 Webhook received for {order_id}: {status}")

    # 3. Logic: Update your database or unlock features
    if status == 'success':
        # logic_to_mark_paid(order_id)
        print(f"✅ Order {order_id} marked as PAID.")
    
    # 4. MMPay requires a 200 OK response to stop retrying
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    # Railway provides the PORT environment variable automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)