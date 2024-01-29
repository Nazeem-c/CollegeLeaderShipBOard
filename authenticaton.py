# from flask import Flask, jsonify, request
# import psycopg2
# import hashlib

# app = Flask(__name__)

# # Assuming you have your database connection parameters defined somewhere
# # Replace these parameters with your actual values
# def db_conn():
#     conn = psycopg2.connect(database = "leadershipp",host="localhost",user="postgres",password="postgres",port="5432");
#     return conn
 
# conn = db_conn()
# cur = conn.cursor()

# # Assuming you have your database cursor defined somewhere
# # Replace this with your actual cursor creation logic
# conn = db_conn()
# cur = conn.cursor()

# @app.route('/signin', methods=['POST'])
# def signin():
#     data = request.get_json()
#     username = data.get('Username')
#     password = data.get('Password')

#     # Hash the password (consider using a stronger hashing algorithm)
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()

#     # Use a prepared statement to protect against SQL injection
#     query = "SELECT * FROM student_auth WHERE Username = %s AND Password = %s"
#     cur.execute(query, (username, hashed_password))
#     user = cur.fetchone()

#     if user:
#         return jsonify({'message': 'Sign-in successful'})
#     else:
#         return jsonify({'message': 'Invalid credentials'}), 401

# if __name__ == '__main__':
#     app.run(debug=True)
