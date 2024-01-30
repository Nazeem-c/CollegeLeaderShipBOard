from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="Leadership", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

conn = db_conn()
cur = conn.cursor()

# ... (Existing code for College, Student, and other routes)

# New route for updating student details
@app.route('/update-student-details/<int:stud_id>', methods=['PUT'])
def update_student_details(stud_id):
    data = request.get_json()

    # Check if c_id and score are provided in the JSON request
    if 'c_id' in data and 'score' in data:
        cur.execute('''
            UPDATE public.attends
            SET score = %s
            WHERE stud_id = %s AND c_id = %s;
        ''', (data['score'], stud_id, data['c_id']))

        conn.commit()

        if cur.rowcount > 0:
            return jsonify({'message': 'Student details updated successfully'})
        else:
            return jsonify({'message': 'No matching record found for the provided stud_id and c_id'})
    else:
        return jsonify({'message': 'Please provide c_id and score in the request'})

# ... (Other routes)

if __name__ == '__main__':
    app.run(debug=True, port=5021)
