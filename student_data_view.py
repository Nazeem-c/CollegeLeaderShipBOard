from flask import Flask, request, jsonify
import psycopg2

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

@app.route('/student/<int:stud_id>', methods=['GET'])
def get_student(stud_id):
    if request.method == 'GET':
        try:
            # Database connection
            connection = db_conn()
            cursor = connection.cursor()

            # Get student details by stud_id
            get_student_query = """
            SELECT s.stud_id, s.stud_name, s.dep_id, s.batch, s.gender, s.clg_id, s.mail, l.username
            FROM student s
            JOIN login l ON s.login_id = l.login_id
            WHERE s.stud_id = %s
            """
            cursor.execute(get_student_query, (stud_id,))
            student_details = cursor.fetchone()

            if not student_details:
                return jsonify({'error': f'Student with ID {stud_id} not found'})

            # Construct the response
            response = {
                'stud_id': student_details[0],
                'stud_name': student_details[1],
                'dep_id': student_details[2],
                'batch': student_details[3],
                'gender': student_details[4],
                'clg_id': student_details[5],
                'mail': student_details[6],
                'username': student_details[7]
            }

            # Close connection
            cursor.close()
            connection.close()

            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
