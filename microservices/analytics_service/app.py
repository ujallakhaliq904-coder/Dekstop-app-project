from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import defaultdict

app = Flask(__name__)
CORS(app)

@app.route('/api/analytics/summary', methods=['POST'])
def get_summary():
    """
    Accepts raw expenses and returns statistical summaries.
    """
    data = request.json
    if not data or 'expenses' not in data:
        return jsonify({"error": "No expenses data provided"}), 400
        
    expenses = data['expenses']
    
    total_spent = sum(e.get('amount', 0) for e in expenses)
    category_totals = defaultdict(float)
    
    for e in expenses:
        cat = e.get('category_name', 'Unknown')
        category_totals[cat] += e.get('amount', 0)
        
    avg_expense = total_spent / len(expenses) if expenses else 0
    
    return jsonify({
        "status": "success",
        "data": {
            "total_spent": round(total_spent, 2),
            "average_expense": round(avg_expense, 2),
            "category_breakdown": dict(category_totals),
            "total_transactions": len(expenses)
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
