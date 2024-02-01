from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Database connection parameters
db_params = {
    'database': 'LeaderShipBoard',
    'host': 'localhost',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432'
}

def db_conn():
    conn = psycopg2.connect(**db_params)
    return conn


conn = db_conn()
cur = conn.cursor()

@app.route('/studaveragescore/<int:stud_id>', methods=['GET'])
def get_student_average_score(stud_id):
    cur.execute('''
        SELECT s.stud_id, s.stud_name, AVG(a.score) AS average_score
        FROM student s
        JOIN score a ON s.stud_id = a.stud_id
        WHERE s.stud_id = %s
        GROUP BY s.stud_id, s.stud_name;
    ''', (stud_id,))
    
    student_average_score = cur.fetchall()
    
    return jsonify({'student_average_score': student_average_score})


if __name__ == '__main__':
    app.run(debug=True)
