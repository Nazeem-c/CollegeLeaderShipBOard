from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
 
# PostgreSQL Configuration
postgresql_config = {
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'database': 'LeaderBoard',
}
 
# Configure Flask to use PostgreSQL with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{postgresql_config["user"]}:{postgresql_config["password"]}@{postgresql_config["host"]}:{postgresql_config["port"]}/{postgresql_config["database"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 


db = SQLAlchemy(app)


class College(db.Model):
    __tablename__ = "College"
    CLG_ID = db.Column(db.Integer, primary_key=True)
    CLG_Name = db.Column(db.String(255), nullable=False)



  
@app.route('/', methods=['GET'])
def get_college():
    Colleges = College.query.all()
    College_list = [{'CLG_ID': College.CLG_ID, 'CLG_NAME': College.CLG_NAME} for College in Colleges]
    return jsonify({'Colleges': College_list})


if __name__ == '__main__':
    app.run(debug=True)