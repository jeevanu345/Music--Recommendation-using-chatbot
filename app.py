from flask import Flask, request, jsonify
from recommendation_model import get_recommendations
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (useful for frontend integration)

# Initialize database
def init_db():
    conn = sqlite3.connect("database/db.sqlite")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        song TEXT NOT NULL,
                        feedback TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.json.get("input", "")
    recommendations = get_recommendations(user_input)
    return jsonify({"recommendations": recommendations})

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.json
    song = data.get("song")
    feedback = data.get("feedback")
    if not song or not feedback:
        return jsonify({"error": "Song and feedback are required"}), 400

    conn = sqlite3.connect("database/db.sqlite")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_feedback (song, feedback) VALUES (?, ?)", (song, feedback))
    conn.commit()
    conn.close()
    return jsonify({"message": "Feedback saved successfully!"})

@app.route('/history', methods=['GET'])
def history():
    conn = sqlite3.connect("database/db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_feedback")
    data = cursor.fetchall()
    conn.close()
    feedback_list = [{"id": row[0], "song": row[1], "feedback": row[2]} for row in data]
    return jsonify({"history": feedback_list})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
