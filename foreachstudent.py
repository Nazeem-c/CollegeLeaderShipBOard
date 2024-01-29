from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# Database connection parameters
db_params = {
    'database': 'leadershipp',
    'host': 'localhost',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432'
}

def db_conn():
    conn = psycopg2.connect(**db_params)
    return conn


conn = db_conn()
cur = conn.cursor()

@app.route('/studaveragescore/<int:stud_id>', methods=['GET'])
def get_topper_dept(stud_id):
    cur.execute('''
        SELECT s.stud_id, s.stud_name, AVG(a.score) AS average_score
        FROM student s
        JOIN attends a ON s.stud_id = a.stud_id
        WHERE s.stud_id = %s
        GROUP BY s.stud_id, s.stud_name;
    ''', (stud_id,))
    
    dept_LeadershipBoard = cur.fetchall()
    
    return jsonify({'LeadershipBoard_department': dept_LeadershipBoard})



# @app.route('/studaveragescore', methods=['GET'])
# def studaveragescore():
#     try:
#         conn = db_conn()
#         cur = conn.cursor()

#         # Get the query parameters from the request
#         stud_id = request.args.get('stud_id')
#         stud_name = request.args.get('stud_name')

#         # Use parameters in the SQL query
#         if stud_id:
#             condition = f's.stud_id = {stud_id}'
#         elif stud_name:
#             condition = f's.stud_name = \'{stud_name}\''
#         else:
#             return jsonify({'error': 'Please provide either stud_id or stud_name as a query parameter.'})

#         query = f'''
#             SELECT s.stud_id, s.stud_name, AVG(a.score) AS average_score
#             FROM student s
#             JOIN attends a ON s.stud_id = a.stud_id
#             WHERE {condition}
#             GROUP BY s.stud_id, s.stud_name;
#         '''

#         cur.execute(query)
#         result = cur.fetchone()

#         if result:
#             student_data = {
#                 'stud_id': result[0],
#                 'stud_name': result[1],
#                 'average_score': result[2]
#             }
#             return jsonify({'student': student_data})
#         else:
#             return jsonify({'message': 'No data found for the provided parameters.'})

#     except Exception as e:
#         return jsonify({'error': str(e)})

#     finally:
#         # Close the database connection
#         if conn:
#             conn.close()

if __name__ == '__main__':
    app.run(debug=True)
