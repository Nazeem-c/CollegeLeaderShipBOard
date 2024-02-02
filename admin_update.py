from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

# Update department
@app.route('/updatedepartment/<int:dep_id>', methods=['PUT'])
def update_department(dep_id):
    try:
        conn = db_conn()
        cur = conn.cursor()

        data = request.get_json()

        # Validate if 'dep_name' is provided and not empty in the JSON data
        if 'dep_name' not in data or not data['dep_name']:
            return jsonify({'error': 'Department name (dep_name) is required and cannot be empty for updating department data'}), 400

        # Update department table
        cur.execute('''
            UPDATE public.department
            SET dep_name = %s
            WHERE dep_id = %s;
        ''', (data['dep_name'], dep_id))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'Department data updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Update college_department

@app.route('/updatecollegedepartment', methods=['PUT'])
def update_college_department():
    try:
        conn = db_conn()
        cur = conn.cursor()

        data = request.get_json()

        # Validate if 'college_clg_id' and 'department_dep_id' are provided in the JSON data
        if 'college_clg_id' not in data or 'department_dep_id' not in data:
            return jsonify({'error': 'College id (college_clg_id) and Department id (department_dep_id) are required for updating college_department data'}), 400

        college_clg_id = request.args.get('college_clg_id')
        department_dep_id = request.args.get('department_dep_id')

        # Update college_department table
        cur.execute('''
            UPDATE public.college_department
            SET college_clg_id = %s, department_dep_id = %s
            WHERE college_clg_id = %s AND department_dep_id = %s;
        ''', (data['college_clg_id'], data['department_dep_id'], college_clg_id, department_dep_id))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'College_department data updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()




# Update semester
@app.route('/updatesemester', methods=['PUT'])
def update_semester():
    try:
        conn = db_conn()
        cur = conn.cursor()

        data = request.get_json()

        # Validate if 'sem_no' and 'sem_id' are provided in the JSON data
        if 'sem_no' not in data or 'sem_id' not in data:
            return jsonify({'error': 'Semester number (sem_no) and Semester id (sem_id) are required for updating semester data'}), 400

        sem_no = request.args.get('sem_no')
        sem_id = request.args.get('sem_id')

        # Update semester table
        cur.execute('''
            UPDATE public.semester
            SET sem_no = %s
            WHERE sem_id = %s;
        ''', (data['sem_no'], sem_id))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'Semester data updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Update student
@app.route('/updatestudent', methods=['PUT'])
def update_student():
    try:
        conn = db_conn()
        cur = conn.cursor()

        data = request.get_json()

        # Validate if 'stud_name' and 'stud_id' are provided in the JSON data
        if 'stud_name' not in data or 'stud_id' not in data:
            return jsonify({'error': 'Student name (stud_name) and Student id (stud_id) are required for updating student data'}), 400

        stud_name = request.args.get('stud_name')
        stud_id = request.args.get('stud_id')

        # Update student table
        cur.execute('''
            UPDATE public.student
            SET stud_name = %s
            WHERE stud_id = %s;
        ''', (stud_name, stud_id))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'Student data updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
     app.run(debug=True, port=5021)