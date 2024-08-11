from app import app, db, User, Project, Image, Video
from datetime import datetime
import random

with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Create 30 dummy users
    users = []
    for i in range(1, 31):
        user = User(
            address=f"{i} Main St",
            email=f"user{i}@example.com",
            image=f"uploads/images/user{i}.jpg",
            lga=f"LGA{i}",
            name=f"User {i}",
            role="User" if i % 2 == 0 else "Admin",
            state=f"State{i}"
        )
        user.set_password("password")
        users.append(user)

    # Add users to the session
    db.session.add_all(users)
    db.session.commit()

    # Create 30 dummy projects
    projects = []
    for i in range(1, 31):
        project = Project(
            category=f"Category{i}",
            contractor=f"Contractor{i}",
            description=f"Description{i}",
            end_date=datetime(2023 + i % 2, 12, 31),
            start_date=datetime(2023, 1, 1),
            name=f"Project {i}",
            latLng=[(random.uniform(-90, 90), random.uniform(-180, 180))],
            user_id=users[i % 30].id
        )
        projects.append(project)

    # Add projects to the session
    db.session.add_all(projects)
    db.session.commit()

    # Create dummy images and videos for projects
    images = []
    videos = []
    for i in range(1, 31):
        image = Image(path=f"uploads/images/project{i}_img1.jpg", project_id=projects[i % 30].id)
        video = Video(path=f"uploads/videos/project{i}_vid1.mp4", project_id=projects[i % 30].id)
        images.append(image)
        videos.append(video)

    # Add images and videos to the session
    db.session.add_all(images)
    db.session.add_all(videos)
    db.session.commit()

    print("30 dummy users and projects inserted successfully!")
