from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.orm import declarative_base

Base = declarative_base()
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number and not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Author phone numbers must be exactly ten digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('title')
    def validate_title(self, key, value):
        if value is None:
            raise ValueError("Post must have a title")

        clickbait_phrases = ["Won't Believe", "Secret", "Guess"]

        if not any(phrase in value for phrase in clickbait_phrases) and not value.startswith("Top "):
            raise ValueError("Title should contain one of the following phrases: 'Won't Believe', 'Secret', 'Guess' or start with 'Top [number]'")

        return value

    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary too long. Must be a maximum of 250 characters.")
        else:
            return summary
    
    @validates('category')
    def validate_category(self, key, value):
        allowed_category = ["Fiction", "Non-Fiction"]
        if value not in allowed_category:
            raise ValueError("Invalid category")
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
