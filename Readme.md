# Inventory Management System

This is an Inventory Management System built with Flask, SQLite3, and various Flask extensions. It supports user authentication, project management, and file uploads.

## Features

- User authentication and management
- Project creation and management
- Image and video uploads
- RESTful API endpoints

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-RESTful
- Flask-Uploads
- Flask-Login
- Flask-Dotenv
- Werkzeug

## Installation

1. **Clone the repository**
2. **Create a virtual environment:**
- python -m venv venv
- source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

- Install the dependencies:
- pip install -r requirements.txt

3. **Set up environment variables: Create a .env file in the root directory and add the following:**
- SECRET_KEY=your_secret_key
- SQLALCHEMY_DATABASE_URI=sqlite:///your_database.db

4. **Initialize the database:**
- flask db init
- flask db migrate -m "Initial migration."
- flask db upgrade

5. **Running the Application**
a. ***Run the Flask application:***
- python app.py

b. ***Access the application:***
- Open your web browser and go to http://127.0.0.1:5000.
- **API Endpoints**
- User Endpoints:
- GET /user: Retrieve all users
- GET /user/<int:user_id>: Retrieve a specific user
- POST /user: Create a new user
- Project Endpoints:
- GET /project: Retrieve all projects
- GET /project/<int:project_id>: Retrieve a specific project
- GET /user/<int:user_id>/projects: Retrieve all projects for a specific user
- POST /project: Create a new project
- File Uploads
- Image Uploads: Images are uploaded to the uploads/images directory.
- Video Uploads: Videos are uploaded to the uploads/videos directory.
## Unit Testing
**To run the unit tests, use the following command:**

- python -m unittest discover

# Contributing
- Contributions are welcome! Please fork the repository and submit a pull request.

# License
- This project is licensed under the MIT License. See the LICENSE file for details.


This `README.md` file provides a comprehensive guide on how to set up, run, and contribute to your Flask application. Let me know if you need any further adjustments or additional information! 😊