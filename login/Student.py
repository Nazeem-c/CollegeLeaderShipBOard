from flask import Flask, jsonify, request,session
import psycopg2
import hashlib
 
app = Flask(__name__)


app.config['SECRET_KEY'] = 'leadershipboard'  # Replace with a secure secret key
 
def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

@app.route('/login_student', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')  # Adjust based on the actual attribute name
    password = data.get('password')
 
    # hashed_password = hashlib.sha256(password.encode()).hexdigest()
 
    query = "SELECT * FROM stud_authentication WHERE username = %s AND password = %s"
 
    try:
        with db_conn() as conn, conn.cursor() as cur:
            cur.execute(query, (username, password))
            user = cur.fetchone()
 
        if user:
            session['username'] = username
            return jsonify({'message': 'Sign-in successful', 'cred_id': user[1]})  # Assuming cred_id is the third column
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
 
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/logout_student')
def logout():
    # Clear the session when the user logs out
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'})    
 
if __name__ == '__main__':
    app.run(debug=True)
 