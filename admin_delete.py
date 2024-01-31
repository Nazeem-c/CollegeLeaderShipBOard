from flask import Flask,jsonify,request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="leadershipp",host="localhost",user="postgres",password="postgres",port="5432")
    return conn
conn = db_conn()
cur = conn.cursor()

@app.route('/delete-department/<int:dep_id>',methods=['DELETE'])
def delete_department(dep_id):
    try:
          # Check if the department with the given ID exists
        cur.execute('SELECT dep_id FROM public.department WHERE dep_id = %s;', (dep_id,))
        existing_department = cur.fetchone()

        if existing_department:
            # Delete from contains table
            cur.execute('DELETE FROM public.contains WHERE dep_id = %s;', (dep_id,))

            # Delete from course table (assuming c_id is a foreign key referencing contains table)
            cur.execute('DELETE FROM public.course WHERE c_id >= 5677 AND c_id IN (SELECT c_id FROM public.contains WHERE dep_id = %s);', (dep_id,))

            # Delete from department table
            cur.execute('DELETE FROM public.department WHERE dep_id = %s;', (dep_id,))

            conn.commit()

            return jsonify({'message': f'Department with ID {dep_id} and associated records deleted successfully'})
        else:
            return jsonify({'message': 'Department not found'})
    except Exception as e :
        conn.rollback()
        return jsonify({'error':str(e)})
    finally :
        cur.close()
        conn.close()
if __name__== '__main__':
    app.run(debug=True,port=5201)
    
