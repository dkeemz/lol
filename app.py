from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
api = Api(app)



#  DB MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    confirm_password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    image = db.Column(db.String(100))
    lga = db.Column(db.String(100))
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(50))
    state = db.Column(db.String(50))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    contractor = db.Column(db.String(100))
    description = db.Column(db.String(200))
    end_date = db.Column(db.DateTime)
    start_date = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    latLng = db.Column(db.PickleType)
    images = db.Column(db.PickleType)  # Store list of image paths
    videos = db.Column(db.PickleType)  # Store list of video paths
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('projects', lazy=True))





# API Resources
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return {
                'address': user.address,
                'email': user.email,
                'image': user.image,
                'lga': user.lga,
                'name': user.name,
                'role': user.role,
                'state': user.state
            }
        else:
            users = User.query.all()
            return [{
                'id': user.id,
                'address': user.address,
                'email': user.email,
                'image': user.image,
                'lga': user.lga,
                'name': user.name,
                'role': user.role,
                'state': user.state
            } for user in users]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('address', required=True)
        parser.add_argument('confirm_password', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('image', required=True)
        parser.add_argument('lga', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('role', required=True)
        parser.add_argument('state', required=True)
        args = parser.parse_args()

        user = User(
            address=args['address'],
            confirm_password=args['confirm_password'],
            email=args['email'],
            image=args['image'],
            lga=args['lga'],
            name=args['name'],
            password=args['password'],
            role=args['role'],
            state=args['state']
        )
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

class ProjectResource(Resource):
    def get(self, project_id=None, user_id=None):
        if project_id:
            project = Project.query.get_or_404(project_id)
            return {
                'category': project.category,
                'contractor': project.contractor,
                'description': project.description,
                'end_date': project.end_date.isoformat(),
                'start_date': project.start_date.isoformat(),
                'name': project.name,
                'latLng': project.latLng,
                'images': project.images,
                'videos': project.videos,
                'user_id': project.user_id
            }
        elif user_id:
            projects = Project.query.filter_by(user_id=user_id).all()
            return [{
                'id': project.id,
                'category': project.category,
                'contractor': project.contractor,
                'description': project.description,
                'end_date': project.end_date.isoformat(),
                'start_date': project.start_date.isoformat(),
                'name': project.name,
                'latLng': project.latLng,
                'images': project.images,
                'videos': project.videos,
                'user_id': project.user_id
            } for project in projects]
        else:
            projects = Project.query.all()
            return [{
                'id': project.id,
                'category': project.category,
                'contractor': project.contractor,
                'description': project.description,
                'end_date': project.end_date.isoformat(),
                'start_date': project.start_date.isoformat(),
                'name': project.name,
                'latLng': project.latLng,
                'images': project.images,
                'videos': project.videos,
                'user_id': project.user_id
            } for project in projects]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('category', required=True)
        parser.add_argument('contractor', required=True)
        parser.add_argument('description', required=True)
        parser.add_argument('end_date', required=True)
        parser.add_argument('start_date', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('latLng', required=True, action='append')
        parser.add_argument('images', required=True, action='append')
        parser.add_argument('videos', required=True, action='append')
        parser.add_argument('user_id', required=True, type=int)
        args = parser.parse_args()

        try:
            project = Project(
                category=args['category'],
                contractor=args['contractor'],
                description=args['description'],
                end_date=datetime.fromisoformat(args['end_date']),
                start_date=datetime.fromisoformat(args['start_date']),
                name=args['name'],
                latLng=args['latLng'],
                images=args['images'],
                videos=args['videos'],
                user_id=args['user_id']
            )
            db.session.add(project)
            db.session.commit()
            return {'message': 'Project created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500






api.add_resource(UserResource, '/user', '/user/<int:user_id>')
api.add_resource(ProjectResource, '/project', '/project/<int:project_id>', '/user/<int:user_id>/projects')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


