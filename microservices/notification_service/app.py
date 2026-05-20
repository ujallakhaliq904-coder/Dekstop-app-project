from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Mock notification queue
notification_log = []

@app.route('/api/notify/budget_alert', methods=['POST'])
def budget_alert():
    """
    Triggers an alert when a user exceeds their budget.
    """
    data = request.json
    user_id = data.get('user_id')
    amount_exceeded = data.get('amount_exceeded')
    
    if not user_id or not amount_exceeded:
        return jsonify({"error": "Missing user_id or amount_exceeded"}), 400
        
    notification = {
        "user_id": user_id,
        "message": f"ALERT: You have exceeded your budget by ${amount_exceeded:.2f}!",
        "timestamp": datetime.now().isoformat(),
        "status": "sent"
    }
    
    notification_log.append(notification)
    
    return jsonify({
        "status": "success",
        "notification": notification
    })

@app.route('/api/notify/logs', methods=['GET'])
def get_logs():
    return jsonify({"logs": notification_log})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
