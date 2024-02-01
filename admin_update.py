from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

# Update department
@app.route('/update-department/<int:dep_id>', methods=['PUT'])
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

@app.route('/update-college-department/<int:college_clg_id>/<int:department_dep_id>', methods=['PUT'])
def update_college_department(college_clg_id, department_dep_id):
    try:
        conn = db_conn()
        cur = conn.cursor()

        data = request.get_json()

        # Validate if 'college_id' and 'dep_id' are provided in the JSON data
        if 'college_id' not in data or 'dep_id' not in data:
            return jsonify({'error': 'College id (college_id) and Department id (dep_id) are required for updating college_department data'}), 400

        # Update college_department table
        cur.execute('''
            UPDATE public.college_department
            SET college_clg_id = %s, department_dep_id = %s
            WHERE college_clg_id = %s AND department_dep_id = %s;
        ''', (data['college_id'], data['dep_id'], college_clg_id, department_dep_id))

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
@app.route('/update-semester/<int:sem_id>', methods=['PUT'])
def update_semester(sem_id):
    try:
        conn = db_conn()
        cur = conn.cursor()

        data = request.get_json()

        # Validate if 'sem_no' is provided and not empty in the JSON data
        if 'sem_no' not in data or not data['sem_no']:
            return jsonify({'error': 'Semester name (sem_no) is required and cannot be empty for updating semester data'}), 400

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
@app.route('/update-student/<int:stud_id>', methods=['PUT'])
def update_student(stud_id):
    try:
        conn = db_conn()
        cur = conn.cursor()

        data = request.get_json()

        # Validate if 'stud_name' is provided and not empty in the JSON data
        if 'stud_name' not in data or not data['stud_name']:
            return jsonify({'error': 'Student name (stud_name) is required and cannot be empty for updating student data'}), 400

        # Update student table
        cur.execute('''
            UPDATE public.student
            SET stud_name = %s
            WHERE stud_id = %s;
        ''', (data['stud_name'], stud_id))

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
