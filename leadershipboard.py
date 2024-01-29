from flask import Flask, jsonify, request
import psycopg2
 
app = Flask(__name__)
 
 
def db_conn():
    conn = psycopg2.connect(database = "leadershipp",host="localhost",user="postgres",password="postgres",port="5432");
    return conn
 
conn = db_conn()
cur = conn.cursor()


@app.route('/leaderboardCollege', methods=['GET'])
def get_college():
    cur.execute('''SELECT s.stud_id, s.stud_name, a.score
FROM student s
JOIN attends a ON s.stud_id = a.stud_id
ORDER BY a.score DESC;
 
''')
    College_LeadershipBOard=cur.fetchall()
    return jsonify({'LeadershipBoard': College_LeadershipBOard})
if __name__ == '__main__':
    app.run(debug=True)