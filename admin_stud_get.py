from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="Leadership", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

conn = db_conn()
cur = conn.cursor()

# ... (Existing code for College, Student, and other routes)

# New route for the given SQL query
@app.route('/student-details/<int:stud_id>', methods=['GET'])
def get_student_details(stud_id):
    cur.execute('''
        SELECT
            student.stud_name,
            college.clg_name,
            department.dep_name,
            course.course_name,
            attends.score
        FROM
            public.student
        JOIN
            public.college ON student.clg_id = college.clg_id
        JOIN
            public.department ON student.dep_id = department.dep_id
        JOIN
            public.attends ON student.stud_id = attends.stud_id
        JOIN
            public.course ON attends.c_id = course.c_id
        WHERE
            student.stud_id = %s;
    ''', (stud_id,))
    
    result = cur.fetchall()

    if result:
        student_data = []
        for row in result:
            student_data.append({
                'stud_name': row[0],
                'clg_name': row[1],
                'dep_name': row[2],
                'course_name': row[3],
                'score': row[4]
            })

        return jsonify({'student_details': student_data})
    else:
        return jsonify({'message': 'No data found'})

# ... (Other routes)

if __name__ == '__main__':
    app.run(debug=True, port=5021)
