# Currency Converter Microservice

This is a lightweight Flask microservice built as a companion API for the Smart Expense Tracker.

## Installation

1. Navigate to this directory:
   ```bash
   cd microservice
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the Flask server:
```bash
python app.py
```
The server will start at `http://127.0.0.1:5000`.

## Endpoints

### 1. Get All Rates
**GET** `/api/rates`
Returns a JSON object with base rates against USD.

### 2. Convert Currency
**GET** `/api/convert?from=USD&to=PKR&amount=50`
Converts 50 USD into PKR based on the configured rates.

**Response Example:**
```json
{
  "query": {
    "amount": 50.0,
    "from": "USD",
    "to": "PKR"
  },
  "result": 13925.0
}
```
