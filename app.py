from flask import Flask, request, jsonify

app = Flask(__name__)

# List to store all transactions
transactions = []

# Dictionary to store balances for each payer
balances = {}

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the Points API. Available endpoints:",
        "endpoints": {
            "/add": "POST - Add points",
            "/spend": "POST - Spend points",
            "/balance": "GET - Get current balances"
        }
    }), 200

@app.route('/add', methods=['POST'])
def add_points():
    """Add points for a specific payer."""
    try:
        data = request.get_json()
        payer = data.get('payer')
        points = data.get('points')
        timestamp = data.get('timestamp')

        # Validate input and Error Handling
        if not payer or not isinstance(points, int) or not timestamp:
            return jsonify({"error": "Invalid input. 'payer', 'points', and 'timestamp' are required."}), 400

        # Update balances
        balances[payer] = balances.get(payer, 0) + points

        # Handle negative points
        if points < 0:
            # Apply negative points to prior transactions
            points_to_adjust = -points
            # Get prior transactions for the payer, sorted by timestamp
            prior_transactions = [t for t in sorted(transactions, key=lambda x: x['timestamp']) if t['payer'] == payer and t['points'] > 0]
            for t in prior_transactions:
                if points_to_adjust <= 0:
                    break
                available_points = t['points']
                deduction = min(available_points, points_to_adjust)
                t['points'] -= deduction
                points_to_adjust -= deduction
        else:
            # For positive points, simply append the transaction
            transactions.append({"payer": payer, "points": points, "timestamp": timestamp})

        # Response Message
        return jsonify({"message": "Transaction added successfully."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/spend', methods=['POST'])
def spend_points():
    """Spend points across payers based on rules."""
    try:
        data = request.get_json()
        points_to_spend = data.get('points')

        if not isinstance(points_to_spend, int) or points_to_spend <= 0:
            return jsonify({"error": "Invalid input. 'points' must be a positive integer."}), 400

        if sum(balances.values()) < points_to_spend:
            return "Insufficient points", 400

        # Sort transactions by timestamp (oldest first)
        sorted_transactions = sorted(transactions, key=lambda x: x['timestamp'])
        spend_details = []
        spent_points = {}

        for transaction in sorted_transactions:
            if points_to_spend <= 0:
                break

            payer = transaction['payer']
            points = transaction['points']

            if payer not in spent_points:
                spent_points[payer] = 0

            # Deduct points based on available balance
            if points > 0:
                deduct_points = min(points, points_to_spend)
                transaction['points'] -= deduct_points
                balances[payer] -= deduct_points
                spent_points[payer] -= deduct_points
                points_to_spend -= deduct_points

        spend_details = [{"payer": payer, "points": points} for payer, points in spent_points.items()]
        return jsonify(spend_details), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/balance', methods=['GET'])
def get_balance():
    """Get current balances for all payers."""
    return jsonify(balances), 200

if __name__ == '__main__':
    app.run(port=8000)
