from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

uri = 'mongodb+srv://davidpp:abc123.@cluster0.4mh62.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
cliente = MongoClient(uri)
db = cliente["PythonUsuarios"]
collection = db["Usuarios"]

#EL ENLACE AL USO
@app.route('/api')
def home():
    return 'Bienvenidos a 2º de Ciclo Superior de Web.'

#ABOUT
@app.route('/api/about')
def about():
    return 'About'

#SACAMOS TODOS LOS USUARIOS.
@app.route('/api/users', methods=['GET'])
def get_users():
    users = list(collection.find({},{"_id":0}))
    return jsonify(users)

#SACAMOS EL PRIMER USUARIO
@app.route('/api/users/user1')
def get_user():
    user = collection.find_one({"id": 1}, {"_id": 0})
    return user
    

#AÑADIMOS UN NUEVO USUARIO
@app.route('/api/users', methods=['POST'])
def add_user():
    users = list(collection.find({},{"_id":0}))
    new_id = len(users)+1
    
    new_user = request.get_json()
    new_user["id"] = new_id

    existe = collection.find_one({"id":new_user['id']})
    if existe:
        return 'Error: El ID ya está en uso'

    collection.insert_one(new_user)
    return jsonify(new_user), 201 #El codigo 201 significa creado.

#ENDPOINT DONDE DEVOLVEMOS EL USUARIO POR SU ID.
@app.route('/api/users/<int:id>', methods=['GET'])
def get_id(id):
    user = collection.find_one({"id": id}, {"_id": 0})
    return user

handle=app