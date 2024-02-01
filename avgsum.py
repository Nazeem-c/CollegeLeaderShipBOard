from flask import Flask, jsonify
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

@app.route('/studaveragescore', methods=['GET'])
def studaveragescore():
    cur.execute('''
        SELECT s.stud_id, s.stud_name, AVG(a.score) AS average_score
        FROM student s
        JOIN score a ON s.stud_id = a.stud_id
        GROUP BY s.stud_id, s.stud_name
        ORDER BY average_score DESC;
    ''')
    
    results = cur.fetchall()

    if results:
        student_list = []
        for result in results:
            student_data = {
                'stud_id': result[0],
                'stud_name': result[1],
                'average_score': result[2]
            }
            student_list.append(student_data)

        return jsonify({'students': student_list})
    else:
        return jsonify({'message': 'No data found'})

if __name__ == '__main__':
    app.run(debug=True)
