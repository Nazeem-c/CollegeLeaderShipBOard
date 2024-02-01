from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

@app.route('/departments', methods=['GET'])
def get_departments():
    try:
        conn = db_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        query = '''
    SELECT d.dep_id, d.dep_name, cd.college_clg_id, cd.department_dep_id, s.sem_no, st.stud_id, st.stud_name, c.course_name
    FROM department d
    LEFT JOIN college_department cd ON d.dep_id = cd.department_dep_id
    LEFT JOIN semester s ON d.dep_id = s.dep_id
    LEFT JOIN student st ON d.dep_id = st.dep_id
    LEFT JOIN course c ON s.sem_id = c.sem_id
'''




        cur.execute(query)
        results = cur.fetchall()

        department_list = []
        for result in results:
            dep_id = result['dep_id']
            dep_name = result['dep_name']
            course_data = {'course_name': result['course_name'], 'sem_no': result['sem_no']}
            student_data = {'stud_id': result['stud_id'], 'stud_name': result['stud_name']}

            # Check if the department is already in the list
            existing_department = next((dep for dep in department_list if dep['dep_id'] == dep_id), None)

            if existing_department:
                existing_department['courses'].append(course_data)
                existing_department['students'].append(student_data)
            else:
                department_data = {'dep_id': dep_id, 'dep_name': dep_name, 'courses': [course_data], 'students': [student_data]}
                department_list.append(department_data)

        return jsonify({'departments': department_list})

    except psycopg2.Error as e:
        # Handle PostgreSQL errors
        return jsonify({'error': f'PostgreSQL error: {e}'})

    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': f'An unexpected error occurred: {e}'})

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
