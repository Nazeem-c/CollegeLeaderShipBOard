from flask import Flask, jsonify, request
import psycopg2
 
app = Flask(__name__)
 
 
 
 
def db_conn():
    conn = psycopg2.connect(database = "LeaderShipBoard",host="localhost",user="postgres",password="postgres",port="5432");
    return conn
 
conn = db_conn()
cur = conn.cursor()
 

 
 
@app.route('/', methods=['GET'])
def get_college():
    cur.execute('''SELECT * FROM college''')
    College=cur.fetchall()
    return jsonify({'College': College})
 
 
 
@app.route('/college', methods=['POST'])
def add_college():
    data = request.get_json()
    clg_id = data['clg_id']
    clg_name = data['clg_name']
 
    cur.execute("INSERT INTO college VALUES (%s,%s)", (clg_id,clg_name))
    conn.commit()
 
    return jsonify({'message': 'College added successfully'})

    
 
 
@app.route('/college/<string:clg_id>', methods=['PUT'])
def update_college(clg_id):
    data = request.get_json()
    new_name = data['clg_name']  # assuming your JSON has a 'new_name' field
 
    cur.execute("UPDATE college SET clg_name = %s WHERE clg_id = %s", (new_name, clg_id))
    conn.commit()
 
    return jsonify({'message': 'college updated successfully'})
 
@app.route('/college/<string:clg_id>', methods=['DELETE'])
def delete_college(clg_id):
    cur.execute("DELETE FROM college WHERE clg_id = %s", (clg_id,))
    conn.commit()
 
    return jsonify({'message': 'College deleted successfully'})
 

 
if __name__ == '__main__':
    app.run(debug=True)