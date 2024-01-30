from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="Leadership", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

conn = db_conn()
cur = conn.cursor()


# New route for deleting student details by student ID
@app.route('/delete-student/<int:stud_id>', methods=['DELETE'])
def delete_student(stud_id):
    try:
        # Check if the student with the given ID exists
        cur.execute('SELECT stud_id FROM public.student WHERE stud_id = %s;', (stud_id,))
        existing_student = cur.fetchone()

        if existing_student:
            # Delete the student
            cur.execute('DELETE FROM public.student WHERE stud_id = %s;', (stud_id,))
            conn.commit()

            return jsonify({'message': f'Student with ID {stud_id} deleted successfully'})
        else:
            return jsonify({'message': 'Student not found'})

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})

# ... (Other routes)

if __name__ == '__main__':
    app.run(debug=True, port=5021)
