from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import io

app = Flask(__name__)
CORS(app)

@app.route('/api/report/csv', methods=['POST'])
def generate_csv_report():
    """
    Accepts JSON data representing expenses and returns a mock CSV generation response.
    """
    data = request.json
    if not data or 'expenses' not in data:
        return jsonify({"error": "No expenses data provided"}), 400
        
    df = pd.DataFrame(data['expenses'])
    # In a real service, this would return the CSV file stream
    csv_string = df.to_csv(index=False)
    
    return jsonify({
        "status": "success",
        "message": "Report generated successfully",
        "data_length": len(df),
        "preview": csv_string[:100] + "..."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
