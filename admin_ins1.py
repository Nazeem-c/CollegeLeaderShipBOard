from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

@app.route('/addCourse', methods=['POST'])
def add_course():
    try:
        conn = db_conn()
        cur = conn.cursor()

        # Extract data for the course table from JSON data
        data = request.get_json()
        course_name = data.get('course_name')

        # Insert data into the course table
        cur.execute('''
            INSERT INTO public.course (course_name)
            VALUES (%s)
            RETURNING course_id;
        ''', (course_name,))
        
        # Fetch the generated course_id
        course_id = cur.fetchone()[0]

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'Course added successfully', 'course_id': course_id})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/addScore', methods=['POST'])
def add_score():
    try:
        conn = db_conn()
        cur = conn.cursor()

        # Extract data for the score table
        stud_id = request.args.get('stud_id')
        course_id = request.args.get('course_id')
        score_value = request.args.get('score_value')

        # Insert data into the score table
        cur.execute('''
            INSERT INTO public.score (stud_id, course_id, score)
            VALUES (%s, %s, %s);
        ''', (stud_id, course_id, score_value))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'Score added successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)

