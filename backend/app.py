from flask import Flask, request, jsonify
import mysql.connector
from config import DB_CONFIG
import logging

app = Flask(__name__)
logging.basicConfig(filename='sqli_attempts.log', level=logging.WARNING)

db = mysql.connector.connect(**DB_CONFIG)

@app.route("/api/search")
def search():
    query = request.args.get("product", "")

    # Basic SQL injection pattern detection
    blacklist = ["'", "--", ";", "/*", "drop", "select", "or 1=1", '"', "union", "#"]
    if any(keyword in query.lower() for keyword in blacklist):
        logging.warning(f"SQLi attempt detected: {query}")
        return jsonify({"error": "Suspicious input detected."}), 400

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE name LIKE %s", ("%" + query + "%",))
    results = cursor.fetchall()
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
