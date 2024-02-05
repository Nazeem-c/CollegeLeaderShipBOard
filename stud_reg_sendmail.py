from flask import Flask, request, jsonify
import psycopg2
import re
import uuid
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Database configuration
db_params = {
    'dbname': 'LeaderShipBoard',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

def db_conn():
    conn = psycopg2.connect(**db_params)
    return conn

def generate_username(stud_name):
    unique_id = str(uuid.uuid4().hex)[:8]
    username = stud_name.lower().replace(' ', '_') + '_' + unique_id
    return username

def generate_password():
    password_length = 8
    password_characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(password_characters) for i in range(password_length))
    return password

def is_email_valid(email):
    # Email validation using a regular expression
    pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return bool(re.match(pattern, email))

def is_email_unique(email, cursor):
    # Check if the email is unique in the database
    query = "SELECT COUNT(*) FROM student WHERE mail = %s"
    cursor.execute(query, (email,))
    count = cursor.fetchone()[0]
    return count == 0

def send_mail(email, username, password, fname, mname, lname):
    recipient_email = email
    
    # SMTP server settings
    smtp_server = 'smtp-relay.brevo.com'
    port = 587  # Change to 465 if using SSL
    smtp_username = 'teamsmv02@gmail.com'
    smtp_password = 'bTOSmPMkJEdpsFL1'
    smtp_sender_email = 'teamsmv02@gmail.com'

    # Create a multipart message
    message = MIMEMultipart()
    message['From'] = smtp_sender_email
    message['To'] = recipient_email
    message['Subject'] = 'Login Credentials - University Portal'

    # Add message body
    body = f"""
Dear {fname} {mname} {lname},

Welcome to the University Portal! Below are your login credentials:

Username: {username}
Temporary Password: {password}

"""
    message.attach(MIMEText(body, 'plain'))

    server = None  # Initialize the variable

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email
        server.send_message(message)
        print(f'Email sent to {recipient_email}!')
    except smtplib.SMTPAuthenticationError as e:
        print(f'Authentication failed. Check your credentials. {e}')
    except smtplib.SMTPException as e:
        print(f'Error while sending email. {e}')
    finally:
        if server:
            # Disconnect from the server
            server.quit()

@app.route('/student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        try:
            data = request.get_json()

            # Check if required fields are present
            required_fields = ['stud_name', 'dep_id', 'batch', 'gender', 'clg_id', 'mail']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'})

            email = data.get('mail')

            # Validate email format
            if not is_email_valid(email):
                return jsonify({'error': 'Invalid email format'})

            # Database connection
            connection = db_conn()
            cursor = connection.cursor()

            # Check if the email is unique
            if not is_email_unique(email, cursor):
                cursor.close()
                connection.close()
                return jsonify({'error': 'Email already exists!'})

            # Generate a simpler random password
            auto_generated_password = generate_password()

            # Generate a username based on the student's name
            username = generate_username(data['stud_name'])

            # Insert into login table
            login_insert_query = """
            INSERT INTO login (password, username, roll)
            VALUES (%s, %s, %s)
            RETURNING login_id
            """
            cursor.execute(login_insert_query, (auto_generated_password, username, 'student'))
            login_id = cursor.fetchone()[0]

            # Insert into student table
            student_insert_query = """
            INSERT INTO student (stud_name, dep_id, batch, gender, clg_id, mail, login_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(student_insert_query, (
                data['stud_name'],
                data['dep_id'],
                data['batch'],
                data['gender'],
                data['clg_id'],
                email,
                login_id
            ))

            # Commit changes and close connection
            connection.commit()
            cursor.close()
            connection.close()

            # Send the email with student details
            send_mail(email, username, auto_generated_password, 
                      data['stud_name'], '', '')  # Add middle and last name if available

            return jsonify({'message': 'Student added successfully!'})
        except psycopg2.IntegrityError as e:
            # Handle specific database integrity constraint violations
            return jsonify({'error': str(e)})
        except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
