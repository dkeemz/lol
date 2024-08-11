from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_restful import Api, Resource, reqparse
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from flask_login import UserMixin, LoginManager
from dotenv import load_dotenv

# Import the database from extensions
from extensions import db

# Import your models
from models import User, Project, Image, Video

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['IMAGE_UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads', 'images')
app.config['VIDEO_UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads', 'videos')

db.init_app(app)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create directories if they don't exist
os.makedirs(app.config['IMAGE_UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['VIDEO_UPLOAD_FOLDER'], exist_ok=True)

# Configure Flask-Uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if file.content_type.startswith('image/'):
            file_path = os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], filename)
        elif file.content_type.startswith('video/'):
            file_path = os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], filename)
        else:
            return 'Unsupported file type', 400
        file.save(file_path)
        return 'File uploaded successfully', 201
    else:
        return 'Unsupported file type', 400

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
        parser.add_argument('email', required=True)
        parser.add_argument('image', type=str, location='files', required=True)
        parser.add_argument('lga', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('role', required=True)
        parser.add_argument('state', required=True)
        args = parser.parse_args()

        image = images.save(request.files['image'])
        image_path = f'uploads/images/{image}'

        user = User(
            address=args['address'],
            email=args['email'],
            image=image_path,
            lga=args['lga'],
            name=args['name'],
            role=args['role'],
            state=args['state']
        )
        user.set_password(args['password'])
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
                'images': [image.path for image in project.images],
                'videos': [video.path for video in project.videos],
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
                'images': [image.path for image in project.images],
                'videos': [video.path for video in project.videos],
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
                'images': [image.path for image in project.images],
                'videos': [video.path for video in project.videos],
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
        parser.add_argument('images', type=str, location='files', action='append', required=True)
        parser.add_argument('videos', required=True, action='append')
        parser.add_argument('user_id', required=True, type=int)
        args = parser.parse_args()

        image_paths = [f'uploads/images/{images.save(image)}' for image in request.files.getlist('images')]

        try:
            project = Project(
                category=args['category'],
                contractor=args['contractor'],
                description=args['description'],
                end_date=datetime.fromisoformat(args['end_date']),
                start_date=datetime.fromisoformat(args['start_date']),
                name=args['name'],
                latLng=args['latLng'],
                images=[Image(path=path) for path in image_paths],
                videos=[Video(path=path) for path in args['videos']],
                user_id=args['user_id']
            )
            db.session.add(project)
            db.session.commit()
            return {'message': 'Project created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

# Register API resources with endpoints
api.add_resource(UserResource, '/user', '/user/<int:user_id>')
api.add_resource(ProjectResource, '/project', '/project/<int:project_id>', '/user/<int:user_id>/projects')

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
