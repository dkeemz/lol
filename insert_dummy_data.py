from datetime import datetime, timedelta
from app import app, db, User, Project, Image, Video
from werkzeug.security import generate_password_hash
import random
import string
import os

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def create_dummy_file(filename, folder):
    file_path = os.path.join(folder, filename)
    with open(file_path, 'wb') as f:
        f.write(os.urandom(1024))  # Create a dummy file with random content
    return file_path

def insert_dummy_data():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        # Create 10 dummy users
        users = []
        for i in range(10):
            image_path = create_dummy_file(f'image{i}.jpg', app.config['IMAGE_UPLOAD_FOLDER'])
            user = User(
                address=f'{random.randint(1, 999)} {random_string(10)} St',
                email=f'user{i}@example.com',
                image=image_path,
                lga=f'LGA{i}',
                name=f'User {i}',
                role=random.choice(['admin', 'user']),
                state=f'State{i}'
            )
            user.set_password(f'password{i}')
            users.append(user)
            db.session.add(user)
        db.session.commit()

        # Create 50 dummy projects
        for i in range(50):
            image_paths = [
                create_dummy_file(f'image{i}_1.jpg', app.config['IMAGE_UPLOAD_FOLDER']),
                create_dummy_file(f'image{i}_2.jpg', app.config['IMAGE_UPLOAD_FOLDER'])
            ]
            video_path = create_dummy_file(f'video{i}.mp4', app.config['VIDEO_UPLOAD_FOLDER'])

            images = [Image(path=path) for path in image_paths]
            videos = [Video(path=video_path)]

            project = Project(
                category=f'Category{i}',
                contractor=f'Contractor{i}',
                description=f'Description of project {i}',
                end_date=datetime.now() + timedelta(days=random.randint(1, 365)),
                start_date=datetime.now() - timedelta(days=random.randint(1, 365)),
                name=f'Project {i}',
                latLng=[random.uniform(-90, 90), random.uniform(-180, 180)],
                images=images,
                videos=videos,
                user_id=random.choice(users).id
            )
            db.session.add(project)
        db.session.commit()

if __name__ == '__main__':
    insert_dummy_data()
