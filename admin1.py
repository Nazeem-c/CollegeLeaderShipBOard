from flask import Flask, jsonify,request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Replace these parameters with your actual database connection details

def db_conn():
    conn = psycopg2.connect(database = "leadershipp",host="localhost",user="postgres",password="postgres",port="5432");
    return conn
 
conn = db_conn()
cur = conn.cursor()

@app.route('/departments', methods=['GET'])
def get_departments():
    cur = conn.cursor(cursor_factory=RealDictCursor)

    query = '''
        SELECT d.dep_id, d.dep_name, c.c_id, c.course_name, ct.sem_no
        FROM department d
        LEFT JOIN contains ct ON d.dep_id = ct.dep_id
        LEFT JOIN course c ON ct.c_id = c.c_id
    '''

    cur.execute(query)
    results = cur.fetchall()

    department_list = []
    for result in results:
        dep_id = result['dep_id']
        dep_name = result['dep_name']
        course_data = {'c_id': result['c_id'], 'course_name': result['course_name'], 'sem_no': result['sem_no']}
        
        # Check if the department is already in the list
        existing_department = next((dep for dep in department_list if dep['dep_id'] == dep_id), None)

        if existing_department:
            existing_department['courses'].append(course_data)
        else:
            department_data = {'dep_id': dep_id, 'dep_name': dep_name, 'courses': [course_data]}
            department_list.append(department_data)

    cur.close()
    conn.close()

    return jsonify({'departments': department_list})






if __name__ == '__main__':
    app.run(debug=True)
