from flask import Flask, jsonify, request
import psycopg2
# from init_db import db_conn

app = Flask(__name__)
def db_conn():
    conn = psycopg2.connect(database = "LeaderShipBoard",host="localhost",user="postgres",password="postgres",port="5432");
    return conn

conn = db_conn()
cur = conn.cursor()


# for finding university topper
@app.route('/leaderboardCollege', methods=['GET'])
def get_topper():
    cur.execute('''SELECT s.stud_id, s.stud_name, a.score
FROM student s
JOIN attends a ON s.stud_id = a.stud_id
ORDER BY a.score DESC;

''')
    College_LeadershipBOard=cur.fetchall()
    return jsonify({'LeadershipBoard': College_LeadershipBOard})




# for finding department topper using dept_id

@app.route('/leaderboardColleges/<string:dep_id>', methods=['GET'])
def get_topper_dept(dep_id):
    cur.execute('''SELECT s.stud_id, s.stud_name, a.score
FROM student s
JOIN attends a ON s.stud_id = a.stud_id
JOIN department d ON s.dep_id = d.dep_id
WHERE d.dep_id = %s
ORDER BY a.score DESC;


''',(dep_id))
    dept_LeadershipBOard=cur.fetchall()
    return jsonify({'LeadershipBoard_department': dept_LeadershipBOard})





# for finding department topper usind dept_name
@app.route('/leaderboardColleges/<string:dep_name>', methods=['GET'])
def get_topper_dept_name(dep_name):
    try:
        cur.execute('''
            SELECT s.stud_id, s.stud_name, a.score
            FROM student s
            JOIN attends a ON s.stud_id = a.stud_id
            JOIN department d ON s.dep_id = d.dep_id
            WHERE d.dep_name = %s
            ORDER BY a.score DESC;
        ''', (dep_name,))

        dept_LeadershipBoard = cur.fetchall()
        return jsonify({'LeadershipBoard_department': dept_LeadershipBoard})

    except Exception as e:
        return jsonify({'error': str(e)}), 500




# for finding department topper,and semesterwise

@app.route('/leaderboardColleges/<string:dep_name>/<int:sem_no>', methods=['GET'])
def get_topper_dept_sem(dep_name, sem_no):
    try:
        cur.execute('''
            SELECT s.stud_id, s.stud_name, a.score
            FROM student s
            JOIN attends a ON s.stud_id = a.stud_id
            JOIN department d ON s.dep_id = d.dep_id
            JOIN contains c ON a.c_id = c.c_id
            JOIN course co ON c.c_id = co.c_id
            WHERE d.dep_name = %s AND c.sem_no = %s
            ORDER BY a.score DESC;
        ''', (dep_name, sem_no))

        dept_LeadershipBoardsem = cur.fetchall()
        return jsonify({'LeadershipBoard_department': dept_LeadershipBoardsem})

    except Exception as e:
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True,port=5000)
