from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Establish a database connection
def db_conn():
    return psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")

# Generic function for deleting records from a table
def delete_record(table_name, primary_key_names, primary_key_values):
    try:
        conn = db_conn()
        cur = conn.cursor()

        # Create a list of conditions for WHERE clause
        conditions = [f'{name} = %s' for name in primary_key_names]
        where_clause = ' AND '.join(conditions)

        # Delete from the specified table
        cur.execute(f'DELETE FROM public.{table_name} WHERE {where_clause};', primary_key_values)
        conn.commit()

        return jsonify({'message': f'Record with {primary_key_names} {primary_key_values} deleted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})
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
@app.route('/delete-department/<int:dep_id>', methods=['DELETE'])
def delete_department(dep_id):
    # Delete records from college_department first
    delete_college_department_by_department(dep_id)
    # Now delete the department
    return delete_record('department', 'dep_id', dep_id)

# Sample delete operation for the college_department table
@app.route('/delete-college-department/<int:college_clg_id>/<int:department_dep_id>', methods=['DELETE'])
def delete_college_department(college_clg_id, department_dep_id):
    column_names = ['college_clg_id', 'department_dep_id']
    return delete_record('college_department', column_names, (college_clg_id, department_dep_id))

# Sample delete operation for the semester table
@app.route('/delete-semester/<int:sem_id>', methods=['DELETE'])
def delete_semester(sem_id):
    column_names = ['sem_id']
    return delete_record('semester', column_names, (sem_id,))

# Sample delete operation for the student table
@app.route('/delete-student/<int:stud_id>', methods=['DELETE'])
def delete_student(stud_id):
    column_names = ['stud_id']
    return delete_record('student', column_names, (stud_id,))


# ... (other routes)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
