from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "PKR": 278.50,
    "INR": 83.30
}

@app.route('/api/rates', methods=['GET'])
def get_rates():
    return jsonify({"base": "USD", "rates": RATES})

@app.route('/api/convert', methods=['GET'])
def convert():
    from_currency = request.args.get('from', 'USD').upper()
    to_currency = request.args.get('to', 'USD').upper()
    amount = float(request.args.get('amount', 0))
    
    if from_currency not in RATES or to_currency not in RATES:
        return jsonify({"error": "Unsupported currency"}), 400

    amount_in_usd = amount / RATES[from_currency]
    converted = amount_in_usd * RATES[to_currency]
    
    return jsonify({"from": from_currency, "to": to_currency, "amount": amount, "result": round(converted, 2)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
