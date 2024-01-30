from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="leadershipp", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

conn = db_conn()
cur = conn.cursor()

# Route to add data to the department table
@app.route('/add-department', methods=['POST'])
def add_department():
    try:
        data = request.get_json()

        dep_name = data.get('dep_name')

        # Insert data into the department table
        cur.execute('''
            INSERT INTO public.department (dep_name)
            VALUES (%s)
            RETURNING dep_id;
        ''', (dep_name,))

        dep_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({'message': 'Department added successfully', 'dep_id': dep_id})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})

# Route to add data to the contains table
@app.route('/add-contains', methods=['POST'])
def add_contains():
    try:
        data = request.get_json()

        c_id = data.get('c_id')
        dep_id = data.get('dep_id')
        sem_no = data.get('sem_no')

        # Insert data into the contains table
        cur.execute('''
            INSERT INTO public.contains (c_id, dep_id, sem_no)
            VALUES (%s, %s, %s)
            RETURNING c_id;
        ''', (c_id, dep_id, sem_no))

        inserted_c_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({'message': 'Contains added successfully', 'c_id': inserted_c_id})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})

# Route to add data to the course table
@app.route('/add-course', methods=['POST'])
def add_course():
    try:
        data = request.get_json()

        course_name = data.get('course_name')

        # Insert data into the course table
        cur.execute('''
            INSERT INTO public.course (course_name)
            VALUES (%s)
            RETURNING c_id;
        ''', (course_name,))

        inserted_c_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({'message': 'Course added successfully', 'c_id': inserted_c_id})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5021)
