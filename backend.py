from flask import Flask, jsonify
import subprocess
import sys
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/run_script', methods=['GET'])
def run_script():
    result = subprocess.run([sys.executable, 'task.py'], capture_output=True, text=True)
    
    # Fetch the latest entry from MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['twitter_trends']
    collection = db['trending']
    latest_entry = collection.find().sort([('_id', -1)]).limit(1)[0]

    # Convert ObjectId to string
    latest_entry['_id'] = str(latest_entry['_id'])

    # Format the response
    formatted_response = {
        "time": latest_entry['date_time'],
        "trends": [
            latest_entry["trend1"],
            latest_entry["trend2"],
            latest_entry["trend3"],
            latest_entry["trend4"],
            latest_entry["trend5"]
        ],
        "ip_address": latest_entry["ip_address"],
        "json_record": latest_entry
    }
    
    # Convert ObjectId to string for JSON serialization
    formatted_response["json_record"]["_id"] = str(formatted_response["json_record"]["_id"])
    
    return jsonify(formatted_response)

if __name__ == '__main__':
    app.run(debug=True)
