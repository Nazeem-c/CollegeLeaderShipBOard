from flask import Flask, jsonify, request,session
import psycopg2
import hashlib
 
app = Flask(__name__)


app.config['SECRET_KEY'] = 'leadershipboard'  
 
def db_conn():
    conn = psycopg2.connect(database="LeaderShipBoard", host="localhost", user="postgres", password="postgres", port="5432")
    return conn

conn = db_conn()
cur = conn.cursor()



# Login route
@app.route('/login_student', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    query = "SELECT * FROM stud_authentication WHERE username = %s AND password = %s"

    try:
        with db_conn() as conn, conn.cursor() as cur:
            cur.execute(query, (username, password))
            user = cur.fetchone()

        if user:
            session['username'] = username
            session['stud_id'] = user[0]  # Assuming user[0] is the stud_id
            return jsonify({'message': 'Sign-in successful', 'cred_id': user[1]})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Student details route
@app.route('/login_student/student-details', methods=['GET'])
def get_student_details():
    try:
        
        if 'username' not in session:
            return jsonify({'message': 'Unauthorized'}), 401

        stud_id = session.get('stud_id')
        
        with db_conn() as conn, conn.cursor() as cur:
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

    except Exception as e:
        return jsonify({'error': str(e)}), 500




# @app.route('/login_student', methods=['POST'])
# def signin():
#     data = request.get_json()
#     username = data.get('username')  
#     password = data.get('password')
 
#     # hashed_password = hashlib.sha256(password.encode()).hexdigest()
 
#     query = "SELECT * FROM stud_authentication WHERE username = %s AND password = %s"
 
#     try:
#         with db_conn() as conn, conn.cursor() as cur:
#             cur.execute(query, (username, password))
#             user = cur.fetchone()
 
#         if user:
#             session['username'] = username
#             return jsonify({'message': 'Sign-in successful', 'cred_id': user[1]})  
#         else:
#             return jsonify({'message': 'Invalid credentials'}), 401
 
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    



# #studentdetails
    
# @app.route('/student-details/<int:stud_id>', methods=['GET'])
# def get_student_details(stud_id):
#     cur.execute('''
#         SELECT
#             student.stud_name,
#             college.clg_name,
#             department.dep_name,
#             course.course_name,
#             attends.score
#         FROM
#             public.student
#         JOIN
#             public.college ON student.clg_id = college.clg_id
#         JOIN
#             public.department ON student.dep_id = department.dep_id
#         JOIN
#             public.attends ON student.stud_id = attends.stud_id
#         JOIN
#             public.course ON attends.c_id = course.c_id
#         WHERE
#             student.stud_id = %s;
#     ''', (stud_id,))
    
#     result = cur.fetchall()

#     if result:
#         student_data = []
#         for row in result:
#             student_data.append({
#                 'stud_name': row[0],
#                 'clg_name': row[1],
#                 'dep_name': row[2],
#                 'course_name': row[3],
#                 'score': row[4]
#             })

#         return jsonify({'student_details': student_data})
#     else:
#         return jsonify({'message': 'No data found'})



# @app.route('/studaveragescore', methods=['GET'])
# def studaveragescore():
#     cur.execute('''
#         SELECT s.stud_id, s.stud_name, AVG(a.score) AS average_score
#         FROM student s
#         JOIN attends a ON s.stud_id = a.stud_id
#         GROUP BY s.stud_id, s.stud_name
#         ORDER BY average_score DESC;
#     ''')
#     results = cur.fetchall()

#     if results:
#         student_list = []
#         for result in results:
#             student_data = {
#                 'stud_id': result[0],
#                 'stud_name': result[1],
#                 'average_score': result[2]
#             }
#             student_list.append(student_data)

#         return jsonify({'students': student_list})
#     else:
#         return jsonify({'message': 'No data found'})




@app.route('/studaveragescore/<int:stud_id>', methods=['GET'])
def studaveragescore(stud_id):
    try:
        # Assuming 'conn' is the connection object and 'cur' is the cursor object
        with db_conn() as conn, conn.cursor() as cur:
            cur.execute('''
                SELECT s.stud_id, s.stud_name, AVG(a.score) AS average_score
                FROM student s
                JOIN attends a ON s.stud_id = a.stud_id
                WHERE s.stud_id = %s
                GROUP BY s.stud_id, s.stud_name;
            ''', (stud_id,))
            results = cur.fetchall()

            if results:
                student_data = {
                    'stud_id': results[0][0],
                    'stud_name': results[0][1],
                    'average_score': results[0][2]
                }
                return jsonify({'student': student_data})
            else:
                return jsonify({'message': f'No data found for student with stud_id {stud_id}'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    
@app.route('/logout_student')
def logout():
    # Clear the session when the user logs out
    session.pop('username', None)
    return jsonify({'message': 'Logout successful'})    
 
if __name__ == '__main__':
    app.run(debug=True)
 
