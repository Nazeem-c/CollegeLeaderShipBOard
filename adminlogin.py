from flask import Flask, jsonify, request
import psycopg2
import hashlib

app = Flask(__name__)

def db_conn():
    return psycopg2.connect(database="Leadership", host="localhost", user="postgres", password="postgres", port="5432")

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    query = "SELECT * FROM public.admin_a WHERE username = %s AND password = %s"

    try:
        with db_conn() as conn, conn.cursor() as cur:
            cur.execute(query, (username, password))
            user = cur.fetchone()

        if user:
            return jsonify({'message': 'Sign-in successful'})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
