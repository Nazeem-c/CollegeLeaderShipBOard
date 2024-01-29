from flask import Flask, jsonify, request, session, redirect, url_for
import psycopg2
import hashlib
import functools

app = Flask(__name__)
app.secret_key = 'secret_key'

def db_conn():
    return psycopg2.connect(database="Leadership", host="localhost", user="postgres", password="postgres", port="5432")

# Admin login required decorator
def admin_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('admin_logged_in'):
            return jsonify({'message': 'Unauthorized'}), 401
        return view(**kwargs)
    return wrapped_view

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    query = "SELECT * FROM public.admin_a WHERE username = %s AND password = %s"

    try:
        with db_conn() as conn, conn.cursor() as cur:
            cur.execute(query, (username, hashed_password))
            user = cur.fetchone()

        if user:
            session['admin_logged_in'] = True
            return jsonify({'message': 'Admin login successful'})
        else:
            return jsonify({'message': 'Invalid admin credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/logout', methods=['GET'])
def admin_logout():
    session.pop('admin_logged_in', None)
    return jsonify({'message': 'Admin logout successful'})

# Protected admin dashboard route
@app.route('/admin/dashboard', methods=['GET'])
@admin_login_required
def admin_dashboard():
    return jsonify({'message': 'Admin dashboard'})

if __name__ == '__main__':
    app.run(debug=True)
