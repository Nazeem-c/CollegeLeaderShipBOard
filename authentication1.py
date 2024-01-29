from flask import Flask, jsonify, request
import psycopg2
import hashlib

app = Flask(__name__)

def db_conn():
    return psycopg2.connect(database="leadershipp", host="localhost", user="postgres", password="postgres", port="5432")

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')  # Adjust based on the actual attribute name
    password = data.get('password')

    hash_password = hashlib.sha256(password.encode()).hexdigest()

    query = "SELECT * FROM student_auth WHERE username = %s AND password = %s"

    try:
        with db_conn() as conn, conn.cursor() as cur:
            cur.execute(query, (username, password))
            user = cur.fetchone()

        if user:
            return jsonify({'message': 'Sign-in successful', 'cred_id': user[1]})  # Assuming cred_id is the third column
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/logout', methods=['POST'])
def logout():
    # Assuming you may want to perform additional logout-related logic here
    # For example, revoking tokens, logging out from other services, etc.
    return jsonify({'message': 'Logout successful'})


if __name__ == '__main__':
    app.run(debug=True)
