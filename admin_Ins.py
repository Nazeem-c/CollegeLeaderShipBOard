from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

conn = db_conn()
cur = conn.cursor()

# Route to add data to the department table
@app.route('/adddepartment', methods=['POST'])
def add_department():
    try:
        data = request.get_json()

        dep_name = data.get('dep_name')

        # Check if dep_name is empty or None
        if not dep_name:
            return jsonify({'error': 'Department name is required', 'message': 'Failed to add department'}), 400

        # Insert data into the department table
        cur.execute('''
            INSERT INTO public.department (dep_name)
            VALUES (%s)
            RETURNING dep_id;
        ''', (dep_name,))

        dep_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({'message': 'Department added successfully', 'dep_id': dep_id})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e), 'message': 'Failed to add department'}), 500


# Route to add data to the college_department table
@app.route('/addcollegedepartment', methods=['POST'])
def add_college_department():
    try:
        data = request.get_json()

        college_clg_id = data.get('college_clg_id')
        department_dep_id = data.get('department_dep_id')

        # Insert data into the college_department table
        cur.execute('''
            INSERT INTO public.college_department (college_clg_id, department_dep_id)
            VALUES (%s, %s);
        ''', (college_clg_id, department_dep_id))

        conn.commit()

        return jsonify({'message': 'College Department added successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e), 'message': 'Failed to add College Department'}), 500


# Route to add data to the semester table
@app.route('/addsemester', methods=['POST'])
def add_semester():
    try:
        data = request.get_json()

        sem_no = data.get('sem_no')
        dep_id = data.get('dep_id')

        # Insert data into the semester table
        cur.execute('''
            INSERT INTO public.semester (sem_no, dep_id)
            VALUES (%s, %s)
            RETURNING sem_id;
        ''', (sem_no, dep_id))

        sem_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({'message': 'Semester added successfully', 'sem_id': sem_id})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e), 'message': 'Failed to add semester'}), 500

# Route to add data to the student table
@app.route('/addstudent', methods=['POST'])
def add_student():
    try:
        data = request.get_json()

        stud_name = data.get('stud_name')
        dep_id = data.get('dep_id')
        batch = data.get('batch')
        gender = data.get('gender')
        clg_id = data.get('clg_id')
        mail = data.get('mail')
        login_id = data.get('login_id')

        # Insert data into the student table
        cur.execute('''
            INSERT INTO public.student (stud_name, dep_id, batch, gender, clg_id, mail, login_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING stud_id;
        ''', (stud_name, dep_id, batch, gender, clg_id, mail, login_id))

        stud_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({'message': 'Student added successfully', 'stud_id': stud_id})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e), 'message': 'Failed to add student'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5021)
