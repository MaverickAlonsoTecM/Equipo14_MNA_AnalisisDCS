import json
import pandas as pd
import mysql.connector
from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

password_path = 'C:/Users/Alberto Patraca/Downloads/password.json'

with open(password_path) as password_file:
    password_dict = json.load(password_file)

miBD = mysql.connector.connect(
  host = "db4free.net",
  user = "a01793469",
  password = password_dict['password'],
  database = "a01793469"
)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/api/user',methods=['GET'])
def getUsers():
    mySQLcursor = miBD.cursor()
    mySQLcursor.execute("SELECT * FROM users")
    resultado = mySQLcursor.fetchall()
    for x in resultado:
        print(x)
    return resultado

@app.route('/api/user',methods=['POST'])
def createUser():
    mySQLcursor = miBD.cursor()

    request_data = request.get_json()
    name = str(request_data['name'])
    password = str(request_data['password'])
    address = str(request_data['address'])
    debts = float(request_data['debts'])
    is_debtor = bool(request_data['is_debtor'])
    mySQLcursor.execute(
        f"INSERT INTO users(name,password,address,debts,is_debtor) VALUES ('{name}','{password}','{address}',{debts},{is_debtor});")
    print("Registro creado exitosamente, se mostrará la tabla:")
    
    mySQLcursor.execute("SELECT * FROM users")
    resultado = mySQLcursor.fetchall()
    for x in resultado:
        print(x)
    return resultado
    
@app.route('/api/user', methods=['PUT'])
def updateUser():
    request_data = request.get_json()
    id = int(request_data['id'])
    
    column_name = str(request_data['column_name'])
    
    if column_name in ['name','password','address']:
        column_value = f"'{str(request_data['column_value'])}'"
    elif column_name == 'debts':
        column_value = float(request_data['column_value'])
    else:
        column_value = bool(request_data['column_value'])
    
    mySQLcursor = miBD.cursor()
    mySQLcursor.execute(
        f"SELECT * FROM users WHERE id = {id};")
    resultado = mySQLcursor.fetchall()
    print(resultado)
    
    if resultado:
        mySQLcursor.execute(f"UPDATE users SET {column_name} = {column_value} WHERE id = {id};")
        mySQLcursor.execute("SELECT * FROM users")
        resultado = mySQLcursor.fetchall()
        for x in resultado:
            print(x)
        return resultado
    return json.dumps({'Warning': f'User id {id} not found'})

@app.route('/api/user', methods=['DELETE'])
def removeUser():
    request_data = request.get_json()
    id = int(request_data['id'])
    
    mySQLcursor = miBD.cursor()
    mySQLcursor.execute(
        f"SELECT * FROM users WHERE id = {id};")
    resultado = mySQLcursor.fetchall()
    print(resultado)
    
    if resultado:
        mySQLcursor.execute(f"DELETE FROM users WHERE id = {id};")
        print(f'Entry #{id} deleted')
        mySQLcursor.execute("SELECT * FROM users")
        resultado = mySQLcursor.fetchall()
        for x in resultado:
            print(x)
        return resultado
    return json.dumps({'Warning': f'User id {id} not found'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)