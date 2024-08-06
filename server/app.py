from flask import Flask, request, jsonify, make_response
from flask_restful import Resource,Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create Flask Object
app = Flask(__name__)

# Create Api instance
api = Api(app)

# Create Database
import sqlite3 as sql
# conn = sql.connect('database.db')
# cur = conn.cursor()
# cur.execute("Create table if not exists Contractor(id INTEGER PRIMARY KEY, first_name VARCHAR(80), last_name VARCHAR(80),project VARCHAR(80))")
# cur.execute("INSERT INTO Contractor (first_name, last_name, project)  VALUES (?,?,?)",['Bob','Builder','Galaxy'])
# conn.commit()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create sqlalchemy mapper
db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    lga = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=False)

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    location = db.Column(db.String(80),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self) -> str:
        return self.Project


class GetUsers(Resource):
    def get(self):
        # users = cur.execute("SELECT * FROM Contractor")
        users = User.query.all()
        user_list = []
        # for user in users.fetchall():
        for user in users:
            user_data = {'id':user.id,'name':user.name,'email':user.email, 'role':user.role,"lga":user.lga,'state':user.state}
            user_list.append(user_data)
            # print(user_list)
        return {'users':user_list}, 200

class GetProjects(Resource):
    def get(self):
        projects = Project.query.all()
        Project_list = []
        for project in projects:
            project_data = {"id":project.id,"name":project.name,"location":project.location,"user_id":project.user_id}
            Project_list.append(project_data)
        return {"projects":Project_list}, 200


class AddUser(Resource):
    def post(self): 
        if request.is_json:
            b = User(name=request.json['name'], email=request.json['email'],password=request.json['password'],role=request.json['role'],lga=request.json['lga'],state=request.json['state'])
            db.session.add(b)
            db.session.commit()
            return make_response(jsonify({id : b.id, 'name' : b.name,'email' : b.email, 'role' : b.role,'password':b.password,"lga":b.lga,"state":b.state}), 201)
        else:
            return {"error":"error must be JSON"}

class AddProject(Resource):
    def post(self): 
        if request.is_json:
            b = Project(name=request.json['name'],location=request.json['location'],user_id=1)
            db.session.add(b)
            db.session.commit()
            return make_response(jsonify({"id":b.id,"name":b.name,"location":b.location, "user_id":b.user_id}), 201)
        else:
            return {"error":"error must be JSON"}
        
class DeleteUser(Resource):
    def delete(self,id):
        if request.is_json:
            user =  User.query.get(id)
            if user is None:
                return {'error':'Not Found'}, 404
            
            db.session.delete(user)
            db.session.commit()
            return f"user with ID:{id} is deleted"
    
class UpdateUser(Resource):
    def put(self, id):
        if request.is_json:
            user = User.query.get(id)
            if user is None:
                return {'error':'Not Found'},404
            else:
                user.first_name=request.json['first_name'] 
                user.last_name=request.json['last_name']
                user.project=request.json['project']

                db.session.commit()
                return f"updated", 200
        else:
            return {"error":"error must be JSON"}



api.add_resource(GetUsers,'/users')
api.add_resource(GetProjects,'/projects')
api.add_resource(AddProject,'/addp')
api.add_resource(AddUser,"/addu")
api.add_resource(DeleteUser,'/deleteu/<int:id>')
api.add_resource(UpdateUser,'/updateu/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)
