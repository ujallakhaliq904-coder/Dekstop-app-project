from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Static mocked exchange rates for simplicity (Base: USD)
RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "PKR": 278.50,
    "INR": 83.30,
    "CAD": 1.36,
    "AUD": 1.52
}

@app.route('/api/rates', methods=['GET'])
def get_rates():
    """Return all available exchange rates."""
    return jsonify({
        "base": "USD",
        "rates": RATES
    })

@app.route('/api/convert', methods=['GET'])
def convert():
    """
    Convert an amount from one currency to another.
    Example: /api/convert?from=USD&to=PKR&amount=100
    """
    from_currency = request.args.get('from', 'USD').upper()
    to_currency = request.args.get('to', 'USD').upper()
    
    try:
        amount = float(request.args.get('amount', 0))
    except ValueError:
        return jsonify({"error": "Invalid amount provided."}), 400
        
    if from_currency not in RATES or to_currency not in RATES:
        return jsonify({"error": "Unsupported currency."}), 400

    # Convert to base (USD) first, then to target currency
    amount_in_usd = amount / RATES[from_currency]
    converted_amount = amount_in_usd * RATES[to_currency]
    
    return jsonify({
        "query": {
            "from": from_currency,
            "to": to_currency,
            "amount": amount
        },
        "result": round(converted_amount, 2)
    })

if __name__ == '__main__':
    # Run the microservice on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
