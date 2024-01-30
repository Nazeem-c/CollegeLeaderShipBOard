from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database = "LeaderShipBoard",host="localhost",user="postgres",password="postgres",port="5432");
    return conn