from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

conn = db_conn()
cur = conn.cursor()

# Route for updating student scores
@app.route('/update-student-score/<int:stud_id>/<int:course_id>', methods=['PUT'])
def update_student_scores(stud_id, course_id):
    try:
        data = request.get_json()

        # Check if the student ID exists
        cur.execute('''
            SELECT COUNT(*) FROM student WHERE stud_id = %s;
        ''', (stud_id,))

        stud_count = cur.fetchone()[0]

        if stud_count == 0:
            return jsonify({'error': 'Student ID does not exist'})

        # Check if the course ID exists
        cur.execute('''
            SELECT COUNT(*) FROM course WHERE course_id = %s;
        ''', (course_id,))

        course_count = cur.fetchone()[0]

        if course_count == 0:
            return jsonify({'error': 'Course ID does not exist'})

        # Assuming data contains the updated score
        new_score = data.get('score')

        # Check if the score is between 0 and 100
        if not (0 <= new_score <= 100):
            return jsonify({'error': 'Score should be between 0 and 100'})

        # Check if the score exists for the given student and course
        cur.execute('''
            SELECT COUNT(*) FROM score WHERE stud_id = %s AND course_id = %s;
        ''', (stud_id, course_id))

        existing_count = cur.fetchone()[0]

        if existing_count == 0:
            return jsonify({'error': 'Score does not exist for the given student and course'})

        # Update the score for the student and course
        cur.execute('''
            UPDATE score
            SET score = %s
            WHERE stud_id = %s AND course_id = %s;
        ''', (new_score, stud_id, course_id))

        # Commit changes to the database
        conn.commit()

        return jsonify({'message': 'Student scores updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# ... (Other routes)

if __name__ == '__main__':
    app.run(debug=True)
