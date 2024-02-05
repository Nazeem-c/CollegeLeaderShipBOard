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

@app.route('/student', methods=['PUT'])
def update_student():
    if request.method == 'PUT':
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

            # Update student information
            update_student_query = """
            UPDATE student
            SET stud_name = %s, dep_id = %s, batch = %s, gender = %s, clg_id = %s, mail = %s
            WHERE stud_id = %s
            """
            cursor.execute(update_student_query, (
                data.get('stud_name', student[1]),
                data.get('dep_id', student[2]),
                data.get('batch', student[3]),
                data.get('gender', student[4]),
                data.get('clg_id', student[5]),
                data.get('mail', student[6]),
                stud_id
            ))

            # Commit changes and close connection
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({'message': f'Student with ID {stud_id} updated successfully!'})
        except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
