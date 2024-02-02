from flask import Flask, jsonify,request
import psycopg2

app = Flask(__name__)

# Establish a database connection
def db_conn():
    return psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")

# Generic function for deleting records from a table
def delete_record(table_name, primary_key_name, primary_key_value):
    try:
        conn = db_conn()
        cur = conn.cursor()

        # Delete from the specified table
        cur.execute(f'DELETE FROM public.{table_name} WHERE {primary_key_name} = %s;', (primary_key_value,))
        conn.commit()

        return jsonify({'message': f'Record with {primary_key_name} {primary_key_value} deleted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# Function to delete records from college_department table by department ID
def delete_college_department_by_department(dep_id):
    try:
        conn = db_conn()
        cur = conn.cursor()

        # Delete from college_department table by department ID
        cur.execute('DELETE FROM public.college_department WHERE department_dep_id = %s;', (dep_id,))
        conn.commit()

        return jsonify({'message': f'Records in college_department referencing department {dep_id} deleted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})
    finally:
        cur.close()
        conn.close()


# Sample delete operation for the department table
@app.route('/deletedepartment', methods=['DELETE'])
def delete_department():
    try:
        # Extract data from query parameters
        dep_id = request.args.get('dep_id')

        # Delete records from college_department first
        delete_college_department_by_department(dep_id)

        # Now delete the department
        return delete_record('department', 'dep_id', dep_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Sample delete operation for the college_department table
@app.route('/deletecollegedepartment', methods=['DELETE'])
def delete_college_department():
    try:
        # Extract data from query parameters
        college_clg_id = request.args.get('college_clg_id')
        department_dep_id = request.args.get('department_dep_id')

        # Convert values to int if needed
        college_clg_id = int(college_clg_id)
        department_dep_id = int(department_dep_id)

        conn = db_conn()
        cur = conn.cursor()

        # Delete from the college_department table
        cur.execute('''
            DELETE FROM public.college_department
            WHERE college_clg_id = %s AND department_dep_id = %s;
        ''', (college_clg_id, department_dep_id))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': f'Record with college_clg_id {college_clg_id} and department_dep_id {department_dep_id} deleted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Sample delete operation for the semester table
@app.route('/deletesemester', methods=['DELETE'])
def delete_semester():
    try:
        # Extract data from query parameters
        sem_id = request.args.get('sem_id')

        # Convert sem_id to int if needed
        sem_id = int(sem_id)

        conn = db_conn()
        cur = conn.cursor()

        # Delete from the semester table
        cur.execute('''
            DELETE FROM public.semester
            WHERE sem_id = %s;
        ''', (sem_id,))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': f'Record with sem_id {sem_id} deleted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# Sample delete operation for the student table
@app.route('/deletestudent', methods=['DELETE'])
def delete_student():
    try:
        # Extract data from query parameters
        stud_id = request.args.get('stud_id')

        # Convert stud_id to int if needed
        stud_id = int(stud_id)

        conn = db_conn()
        cur = conn.cursor()

        # Delete from the student table
        cur.execute('''
            DELETE FROM public.student
            WHERE stud_id = %s;
        ''', (stud_id,))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': f'Record with stud_id {stud_id} deleted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()



# ... (other routes)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
