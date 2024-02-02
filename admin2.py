from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn
@app.route('/courseStats', methods=['GET'])
def fetch_course_scores():
    try:
        conn = db_conn()
        cur = conn.cursor()

        # Perform a JOIN operation on course_id to fetch data from both tables
        cur.execute('''
            SELECT course.course_id, course.course_name, score.stud_id, score.score
            FROM public.course
            JOIN public.score ON course.course_id = score.course_id;
        ''')

        # Fetch all the results
        result = cur.fetchall()

        # Convert the result to a list of dictionaries for JSON response
        data = [{'course_id': row[0], 'course_name': row[1], 'stud_id': row[2], 'score': row[3]} for row in result]

        return jsonify({'data': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
