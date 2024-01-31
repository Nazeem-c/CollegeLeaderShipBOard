from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="Leadership", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

@app.route('/update-department/<int:dep_id>', methods=['PUT'])
def update_department(dep_id):
    data = request.get_json()

    try:
        conn = db_conn()
        cur = conn.cursor()

        # Update department table
        cur.execute('''
            UPDATE public.department
            SET dep_name = %s
            WHERE dep_id = %s;
        ''', (data['dep_name'], dep_id))

        # Commit the transaction
        conn.commit()

        return jsonify({'message': 'Department data updated successfully'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5021)
