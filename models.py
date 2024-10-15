from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import  MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    
    })

db = SQLAlchemy(metadata=metadata)

# Association table
user_groups = db.Table('user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-posts.user',)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    posts = db.relationship('Post', back_populates='user', lazy=True)
    groups = db.relationship('Group', secondary=user_groups, back_populates='users', lazy=True)

    @validates('email')
    def validate_email(self, key, value):
        if '@' not in value:
            raise ValueError("Invalid email address")
        return value

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    serialize_rules = ('-user.posts', '-users.groups', )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)  # Changed unique=True to nullable=False for description
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Moved this line into the class
    user = db.relationship('User', back_populates='posts', lazy=True)

class Group(db.Model, SerializerMixin):
    __tablename__ = 'groups'

    serialize_rules = ('-users.groups',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    users = db.relationship('User', secondary=user_groups, back_populates='groups', lazy=True)
