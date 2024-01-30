from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="Leadership", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

conn = db_conn()
cur = conn.cursor()


# New route for inserting student details
@app.route('/add-student', methods=['POST'])
def add_student():
    try:
        data = request.get_json()

        stud_name = data['stud_name']
        batch = data['batch']
        gender = data['gender']
        dep_id = data['dep_id']
        clg_id = data['clg_id']

        # Inserting data into the database
        cur.execute('''
            INSERT INTO public.student (stud_name, batch, gender, dep_id, clg_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING stud_id;
        ''', (stud_name, batch, gender, dep_id, clg_id))

        stud_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({'message': 'Student added successfully', 'stud_id': stud_id})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})

# ... (Other routes)

if __name__ == '__main__':
    app.run(debug=True, port=5021)
