from flask import Flask, jsonify, request
import psycopg2
app = Flask(__name__)
 
 
 




 
 
def db_conn():
    conn = psycopg2.connect(database = "Leadership",host="localhost",user="postgres",password="postgres",port="5432");
    return conn
 
conn = db_conn()
cur = conn.cursor()
 
#----------------------------------------beg----college------------------------------------------------------------------------------------------------------------------


@app.route('/', methods=['GET'])
def get_college():
    cur.execute('''SELECT * FROM College''')
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
 

# @app.route('/college', methods=['POST'])
# def add_college():
#     data = request.get_json()
#     clg_id = data['clg_id']
#     clg_name = data['clg_name']
 
#     cur.execute("INSERT INTO college VALUES (%s,%s)", (clg_id,clg_name))
#     conn.commit()
 
#     return jsonify({'message': 'College added successfully'})


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


#----------------------------------------end----college------------------------------------------------------------------------------------------------------------------



#----------------------------------------beg----student------------------------------------------------------------------------------------------------------------------

@app.route('/student/', methods=['GET'])
def get_student():
    cur.execute('''SELECT * FROM student''')
    student=cur.fetchall()
    return jsonify({'student': student})




 
 #----------------------------------------end----student------------------------------------------------------------------------------------------------------------------

#----------------------------------------beg----filter on scored-----------------------------------------------------------------------------------------------------------------
@app.route('/studtopscore', methods=['GET'])
def studtopscore():
    cur.execute('''
        SELECT s.stud_id, s.stud_name, MAX(a.score) AS top_score
        FROM student s
        JOIN attends a ON s.stud_id = a.stud_id
        GROUP BY s.stud_id, s.stud_name
        ORDER BY top_score DESC
        LIMIT 1;
    ''')
    result = cur.fetchone()

    if result:
        student_data = {
            'stud_id': result[0],
            'stud_name': result[1],
            'top_score': result[2]
        }
        return jsonify({'student': student_data})
    else:
        return jsonify({'message': 'No data found'})




#----------------------------------------end----filter on score-------------------------------------------------------------------------------------------------------------------
#----------------------------------------beg----sum on scored-----------------------------------------------------------------------------------------------------------------

@app.route('/studtotalscore', methods=['GET'])
def studtotalscore():
    cur.execute('''
        SELECT s.stud_id, s.stud_name, SUM(a.score) AS total_score
        FROM student s
        JOIN attends a ON s.stud_id = a.stud_id
        GROUP BY s.stud_id, s.stud_name
        ORDER BY total_score DESC;
    ''')
    results = cur.fetchall()

    if results:
        student_list = []
        for result in results:
            student_data = {
                'stud_id': result[0],
                'stud_name': result[1],
                'total_score': result[2]
            }
            student_list.append(student_data)

        return jsonify({'students': student_list})
    else:
        return jsonify({'message': 'No data found'})

#----------------------------------------end----sum on scored-----------------------------------------------------------------------------------------------------------------
 
# -----------------------------------------------------------for finding university topper-----------------------------------------------------------------------------------------------------------------
@app.route('/leaderboardCollege', methods=['GET'])
def get_topper():
    cur.execute('''SELECT s.stud_id, s.stud_name, a.score
FROM student s
JOIN attends a ON s.stud_id = a.stud_id
ORDER BY a.score DESC;
 
''')
    College_LeadershipBOard=cur.fetchall()
    return jsonify({'LeadershipBoard': College_LeadershipBOard})
 
#----------------------------------------end- for finding university topper----------------------------------------------------------------------------------------------------------------

 
# ------------------------------------------------------------for finding department topper using dept_id------------------------------------------------------------
 
@app.route('/leaderboardCollegedepartment/<string:dep_id>', methods=['GET'])
def get_topper_dept(dep_id):
    cur.execute('''SELECT s.stud_id, s.stud_name, a.score
FROM student s
JOIN attends a ON s.stud_id = a.stud_id
JOIN department d ON s.dep_id = d.dep_id
WHERE d.dep_id = %s
ORDER BY a.score DESC;
 
 
''',(dep_id))
    dept_LeadershipBOard=cur.fetchall()
    return jsonify({'LeadershipBoard_department': dept_LeadershipBOard})
 
 
# ------------------------------------------------------------for finding department topper using dept_id--------------------------------------------------------------------------------------------------------------
# Admin login route


if __name__ == '__main__':
    app.run(debug=True,port=5021)




  