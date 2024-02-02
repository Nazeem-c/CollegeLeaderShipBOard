from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

@app.route('/courseupdate', methods=['PUT'])
def update_course():
    try:
        conn = db_conn()
        cur = conn.cursor()

        # Extract data from query parameters
        course_id = request.args.get('course_id')
        course_name = request.args.get('course_name')

        # Update data in the course table
        cur.execute('''
            UPDATE public.course
            SET course_name = %s
            WHERE course_id = %s;
        ''', (course_name, course_id))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'Course updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/scoreupdate', methods=['PUT'])
def update_score():
    try:
        conn = db_conn()
        cur = conn.cursor()

        # Extract data from query parameters
        course_id = request.args.get('course_id')
        stud_id = request.args.get('stud_id')
        score_value = request.args.get('score')

        # Update data in the score table
        cur.execute('''
            UPDATE public.score
            SET stud_id = %s, score = %s
            WHERE course_id = %s;
        ''', (stud_id, score_value, course_id))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'Score updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
