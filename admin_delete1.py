from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

def delete_score_record(course_id):
    try:
        conn = db_conn()
        cur = conn.cursor()

        # Delete records from the 'score' table
        cur.execute('DELETE FROM public.score WHERE course_id = %s;', (course_id,))
        conn.commit()

        return jsonify({'message': f'Records in the score table for course_id {course_id} deleted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

def delete_course_record(course_id):
    try:
        conn = db_conn()
        cur = conn.cursor()

        # Delete the record from the 'course' table
        cur.execute('DELETE FROM public.course WHERE course_id = %s;', (course_id,))
        conn.commit()

        return jsonify({'message': f'Record in the course table with course_id {course_id} deleted successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/deletescore', methods=['DELETE'])
def delete_score():
    course_id = request.args.get('course_id')
    return delete_score_record(course_id)

@app.route('/deletecourse', methods=['DELETE'])
def delete_course():
    course_id = request.args.get('course_id')
    return delete_course_record(course_id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
