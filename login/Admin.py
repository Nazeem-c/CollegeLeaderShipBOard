


from flask import Flask, jsonify, request, redirect, url_for, session
import psycopg2
import hashlib
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'leadershipboard'  # Replace with a secure secret key

def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn


conn = db_conn()
cur = conn.cursor()

# -------------------------------------------------------------------admin login--------------------------------------------------------------

@app.route('/login_admin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('admin_id')
    password = data.get('admin_password')
 
    # hashed_password = hashlib.sha256(password.encode()).hexdigest()
 
    query = "SELECT * FROM admin WHERE admin_id = %s AND admin_password = %s"
 
    try:
        with db_conn() as conn, conn.cursor() as cur:
            cur.execute(query, (username, password))
            user = cur.fetchone()
 
        if user:
            # For demonstration purposes, store the username in the session
            session['username'] = username
            return jsonify({'message': 'Sign-in successful', 'password': user[1]})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
 
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ------------------------------------------------------------college------------------------------------------------------------------------


# for viewing list of every college

@app.route('/collegelist', methods=['GET'])
def get_college():
    cur.execute('''SELECT * FROM college''')
    College=cur.fetchall()
    return jsonify({'College': College})



@app.route('/add_college', methods=['POST'])
def add_college():
    data = request.get_json()
    clg_id = data['clg_id']
    clg_name = data['clg_name']
 
    cur.execute("INSERT INTO college VALUES (%s,%s)", (clg_id,clg_name))
    conn.commit()
 
    return jsonify({'message': 'College added successfully'})




@app.route('/update_college/<string:clg_id>', methods=['PUT'])
def update_college(clg_id):
    data = request.get_json()
    new_name = data['clg_name']  
 
    cur.execute("UPDATE college SET clg_name = %s WHERE clg_id = %s", (new_name, clg_id))
    conn.commit()
 
    return jsonify({'message': 'college updated successfully'})




@app.route('/college/<string:clg_id>', methods=['DELETE'])
def delete_college(clg_id):
    cur.execute("DELETE FROM college WHERE clg_id = %s", (clg_id,))
    conn.commit()
 
    return jsonify({'message': 'College deleted successfully'})





# logout
@app.route('/logout_admin')
def logout():
    # Clear the session when the user logs out
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'})

if __name__ == '__main__':
    app.run(debug=True)




