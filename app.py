from flask import Flask, make_response, jsonify, request
from models import *  # Ensure proper import of your models
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)

# TO CONFIGURE -> CREATE DATABASE CONNECTION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Add this to suppress warnings

# Creating an instance for migrate
migrate = Migrate(app, db)
db.init_app(app)

# Creating a route
@app.route('/')
def index():
    return "Welcome to Flask"

# Route to handle both GET and POST for users
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # Fetch and return all users
        users = User.query.all()
        response = [user.to_dict() for user in users]
        return make_response(jsonify(response), 200)

    if request.method == 'POST':
        # Handle user creation
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()

        return make_response({'message': 'User created successfully'}, 201)

@app.route('/users/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def user(id):
    if request.method == 'GET':
        user = User.query.get(id)
        return make_response(user.to_dict(), 200)      
  

# Route to handle both GET and POST for posts
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'GET':
        # Fetch and return all posts
        posts = Post.query.all()
        response = [post.to_dict() for post in posts]
        return make_response(jsonify(response), 200)

    if request.method == 'POST':
        # Handle post creation
        data = request.get_json()
        new_post = Post(title=data['title'], content=data['content'])
        db.session.add(new_post)
        db.session.commit()

        return make_response({'message': 'Post created successfully'}, 201)

# Running the app
if __name__ == '__main__':
    app.run(port=8080, debug=True)
