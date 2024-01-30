


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
  
    query = """
        SELECT c.clg_id, c.clg_name, c.contact, c.established_year, a.place, a.state, a.pin
        FROM college c
        JOIN address a ON c.addr_id = a.addr_id
    """

    with db_conn() as conn, conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()

    colleges = []

    for result in results:
    
        clg_id, clg_name, contact, established_year, place, state, pin = result

        college_info = {
            'clg_id': clg_id,
            'clg_name': clg_name,
            'contact': contact,
            'established_year': established_year,
            'place': place,
            'state': state,
            'pin': pin
        }

        colleges.append(college_info)

    return jsonify({'colleges': colleges})

# add college

@app.route('/add_college', methods=['POST'])
def add_college():
    data = request.get_json()

    clg_name = data['clg_name']
    contact = data['contact']
    established_year = data['established_year']
    place = data['place']
    state = data['state']
    pin = data['pin']

    
    query_check_duplicate = "SELECT clg_id FROM college WHERE clg_name = %s"
    
    with db_conn() as conn, conn.cursor() as cur:
        cur.execute(query_check_duplicate, (clg_name,))
        existing_clg_id = cur.fetchone()

        if existing_clg_id:
            return jsonify({'message': 'College with the same name already exists'}), 400

   
    query_address = "INSERT INTO address (place, state, pin) VALUES (%s, %s, %s) RETURNING addr_id"

    with db_conn() as conn, conn.cursor() as cur:
        cur.execute(query_address, (place, state, pin))
        addr_id = cur.fetchone()[0]


    query_college = "INSERT INTO college (clg_name, contact, established_year, addr_id) VALUES (%s, %s, %s, %s)"

    with db_conn() as conn, conn.cursor() as cur:
        cur.execute(query_college, (clg_name, contact, established_year, addr_id))
        conn.commit()

    return jsonify({'message': 'College added successfully'})



# update college
@app.route('/update_college/<int:clg_id>', methods=['PUT'])
def update_college(clg_id):
    data = request.get_json()

    clg_name = data.get('clg_name')
    contact = data.get('contact')
    established_year = data.get('established_year')
    place = data.get('place')
    state = data.get('state')
    pin = data.get('pin')

    query_check_existence = "SELECT clg_id FROM college WHERE clg_id = %s"
    
    with db_conn() as conn, conn.cursor() as cur:
        cur.execute(query_check_existence, (clg_id,))
        existing_clg_id = cur.fetchone()

        if not existing_clg_id:
            return jsonify({'message': 'College not found'}), 404

    query_update_address = "UPDATE address SET place = %s, state = %s, pin = %s WHERE addr_id = (SELECT addr_id FROM college WHERE clg_id = %s)"

    with db_conn() as conn, conn.cursor() as cur:
        cur.execute(query_update_address, (place, state, pin, clg_id))


    query_update_college = "UPDATE college SET clg_name = %s, contact = %s, established_year = %s WHERE clg_id = %s"

    with db_conn() as conn, conn.cursor() as cur:
        cur.execute(query_update_college, (clg_name, contact, established_year, clg_id))
        conn.commit()

    return jsonify({'message': 'College updated successfully'})


# delete college 
@app.route('/delete_college/<int:clg_id>', methods=['DELETE'])
def delete_college(clg_id):
   query_check_existence = "SELECT clg_id, addr_id FROM college WHERE clg_id = %s"

    
   cur.execute(query_check_existence, (clg_id,))
   college_info = cur.fetchone()

   if not college_info:
            return jsonify({'message': 'College not found'}), 404

   addr_id = college_info[1]

        # Check if the college has references in college_department
   query_check_references = "SELECT 1 FROM college_department WHERE clg_id = %s LIMIT 1"
   cur.execute(query_check_references, (clg_id,))
   references_exist = bool(cur.fetchone())

        # If references exist, return an error
   if references_exist:
            return jsonify({'error': 'College has references in college_department, delete them first'}), 400

        # If no references, update data in the 'college' table to remove the foreign key constraint
   query_update_college = "UPDATE college SET addr_id = NULL WHERE clg_id = %s"
   cur.execute(query_update_college, (clg_id,))

        # Check if the college has a valid addr_id before proceeding with deletion
   if addr_id is not None:
            # Delete data from the 'address' table
            query_delete_address = "DELETE FROM address WHERE addr_id = %s"
            cur.execute(query_delete_address, (addr_id,))

    # Delete data from the 'college' table
   query_delete_college = "DELETE FROM college WHERE clg_id = %s"
   with db_conn() as conn, conn.cursor() as cur:
        cur.execute(query_delete_college, (clg_id,))
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




