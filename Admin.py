


from flask import Flask, jsonify, request, redirect, url_for, session
import psycopg2
import hashlib
from psycopg2.extras import RealDictCursor 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'leadershipboard'  # Replace with a secure secret key

def db_conn():
    conn = psycopg2.connect(database = "Leadership",host="localhost",user="postgres",password="postgres",port="5432");
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





#----------------------------------------------------------------------department&Course----------------------------------------------------------

@app.route('/departments', methods=['GET'])
def get_departments():
    cur = conn.cursor(cursor_factory=RealDictCursor)

    query = '''
        SELECT d.dep_id, d.dep_name, c.c_id, c.course_name, ct.sem_no
        FROM department d
        LEFT JOIN contains ct ON d.dep_id = ct.dep_id
        LEFT JOIN course c ON ct.c_id = c.c_id
    '''

    cur.execute(query)
    results = cur.fetchall()

    department_list = []
    for result in results:
        dep_id = result['dep_id']
        dep_name = result['dep_name']
        course_data = {'c_id': result['c_id'], 'course_name': result['course_name'], 'sem_no': result['sem_no']}
        
        # Check if the department is already in the list
        existing_department = next((dep for dep in department_list if dep['dep_id'] == dep_id), None)

        if existing_department:
            existing_department['courses'].append(course_data)
        else:
            department_data = {'dep_id': dep_id, 'dep_name': dep_name, 'courses': [course_data]}
            department_list.append(department_data)

  

    return jsonify({'departments': department_list})




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
    

#----------------------------------------------------------------------student--------------------------------------------------------------------

# New route for the given SQL query
@app.route('/student-details/<int:stud_id>', methods=['GET'])
def get_student_details(stud_id):
    cur.execute('''
        SELECT
            student.stud_name,
            college.clg_name,
            department.dep_name,
            course.course_name,
            attends.score
        FROM
            public.student
        JOIN
            public.college ON student.clg_id = college.clg_id
        JOIN
            public.department ON student.dep_id = department.dep_id
        JOIN
            public.attends ON student.stud_id = attends.stud_id
        JOIN
            public.course ON attends.c_id = course.c_id
        WHERE
            student.stud_id = %s;
    ''', (stud_id,))
    
    result = cur.fetchall()

    if result:
        student_data = []
        for row in result:
            student_data.append({
                'stud_name': row[0],
                'clg_name': row[1],
                'dep_name': row[2],
                'course_name': row[3],
                'score': row[4]
            })

        return jsonify({'student_details': student_data})
    else:
        return jsonify({'message': 'No data found'})


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




# New route for updating student details
@app.route('/update-student-details/<int:stud_id>', methods=['PUT'])
def update_student_details(stud_id):
    data = request.get_json()

    # Check if c_id and score are provided in the JSON request
    if 'c_id' in data and 'score' in data:
        cur.execute('''
            UPDATE public.attends
            SET score = %s
            WHERE stud_id = %s AND c_id = %s;
        ''', (data['score'], stud_id, data['c_id']))

        conn.commit()

        if cur.rowcount > 0:
            return jsonify({'message': 'Student details updated successfully'})
        else:
            return jsonify({'message': 'No matching record found for the provided stud_id and c_id'})
    else:
        return jsonify({'message': 'Please provide c_id and score in the request'})

# New route for deleting student details by student ID
@app.route('/delete-student/<int:stud_id>', methods=['DELETE'])
def delete_student(stud_id):
    try:
        # Check if the student with the given ID exists
        cur.execute('SELECT stud_id FROM public.student WHERE stud_id = %s;', (stud_id,))
        existing_student = cur.fetchone()

        if existing_student:
            # Delete the student
            cur.execute('DELETE FROM public.student WHERE stud_id = %s;', (stud_id,))
            conn.commit()

            return jsonify({'message': f'Student with ID {stud_id} deleted successfully'})
        else:
            return jsonify({'message': 'Student not found'})

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)})



# logout
@app.route('/logout_admin')
def logout():
    # Clear the session when the user logs out
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'})

if __name__ == '__main__':
    app.run(debug=True)