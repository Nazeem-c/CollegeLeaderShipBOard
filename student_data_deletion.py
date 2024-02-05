from flask import Flask, request, jsonify
import psycopg2
import re
import uuid
import random
import string

app = Flask(__name__)

# Database configuration 
db_params = {
    'dbname': 'LeaderShipBoard',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

def db_conn():
    conn = psycopg2.connect(**db_params)
    return conn

@app.route('/student', methods=['DELETE'])
def delete_student(stud_id):
    if request.method == 'DELETE':
        try:

            stud_id = request.args.get("stud_id")
            data = request.get_json()


            # Database connection
            connection = db_conn()
            cursor = connection.cursor()

            # Check if student exists
            check_student_query = "SELECT * FROM student WHERE stud_id = %s"
            cursor.execute(check_student_query, (stud_id,))
            student = cursor.fetchone()

            if not student:
                return jsonify({'error': f'Student with ID {stud_id} not found'})

            # Get login_id associated with the student
            login_id_query = "SELECT login_id FROM student WHERE stud_id = %s"
            cursor.execute(login_id_query, (stud_id,))
            login_id = cursor.fetchone()[0]

            # Delete from student table
            delete_student_query = "DELETE FROM student WHERE stud_id = %s"
            cursor.execute(delete_student_query, (stud_id,))

            # Commit changes to the student table
            connection.commit()

            # Delete from login table using the fetched login_id
            delete_login_query = "DELETE FROM login WHERE login_id = %s"
            cursor.execute(delete_login_query, (login_id,))

            # Commit changes and close connection
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({'message': 'Student deleted successfully!'})
        except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
