from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Replace these values with your actual database connection parameters
conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
cur = conn.cursor()

# Function to check if a student with given ID exists
def student_exists(stud_id):
    cur.execute('SELECT 1 FROM public.student WHERE stud_id = %s;', (stud_id,))
    return cur.fetchone() is not None

# Function to check if a course with given ID exists
def course_exists(course_id):
    cur.execute('SELECT 1 FROM public.course WHERE course_id = %s;', (course_id,))
    return cur.fetchone() is not None

# Function to get course information for the given student along with the score
def get_course_info(stud_id):
    try:
        if not student_exists(stud_id):
            return jsonify({'error': f'Student with ID {stud_id} not found.'})

        cur.execute('''
            SELECT c.course_id, c.course_name, sc.score
            FROM public.course c
            JOIN public.semester s ON c.sem_id = s.sem_id
            LEFT JOIN public.score sc ON c.course_id = sc.course_id AND sc.stud_id = %s
            WHERE s.dep_id = (
                SELECT dep_id
                FROM public.student
                WHERE stud_id = %s
            );
        ''', (stud_id, stud_id))

        courses_info = cur.fetchall()

        if not courses_info:
            return jsonify({'error': 'No courses found for the given student.'})

        return jsonify({'stud_id': stud_id, 'courses': [{'course_id': course[0], 'course_name': course[1], 'score': course[2]} for course in courses_info]})
    
    except Exception as e:
        return jsonify({'error': str(e)})

# Function to insert score for a given student and course
def insert_score(stud_id, course_id, score):
    try:
        if not student_exists(stud_id):
            return jsonify({'error': f'Student with ID {stud_id} not found.'})

        if not course_exists(course_id):
            return jsonify({'error': f'Course with ID {course_id} not found.'})

        # Check if the score is between 0 and 100
        if not (0 <= score <= 100):
            return jsonify({'error': 'Score should be between 0 and 100.'})

        # Check if the record already exists
        cur.execute('SELECT score FROM public.score WHERE stud_id = %s AND course_id = %s;', (stud_id, course_id))
        existing_score = cur.fetchone()

        if existing_score:
            return jsonify({'message': f'Score {existing_score[0]} already exists for the given student and course.'})
        else:
            # Insert a new record if it doesn't exist
            cur.execute('INSERT INTO public.score (stud_id, course_id, score) VALUES (%s, %s, %s);', (stud_id, course_id, score))
            conn.commit()
            return jsonify({'message': 'Score inserted successfully'})
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})

# Combined route for both GET and POST
@app.route('/student-course/<int:stud_id>', methods=['GET', 'POST'])
def student_course(stud_id):
    if request.method == 'GET':
        return get_course_info(stud_id)
    elif request.method == 'POST':
        data = request.get_json()
        course_id = data.get('course_id')
        score = data.get('score')

        if course_id is None or score is None:
            return jsonify({'error': 'Both course_id and score are required for score insertion.'})

        return insert_score(stud_id, course_id, score)

# ... (Other routes)

if __name__ == '__main__':
    app.run(debug=True)

# Close the cursor and connection when the application shuts down
@app.teardown_appcontext
def close_connection(exception=None):
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
