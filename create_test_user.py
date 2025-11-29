from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Check if the user already exists
    if User.query.filter_by(username='testuser').first() is None:
        # Create a new user
        new_user = User(
            username='testuser',
            email='testuser@example.com',
        )
        new_user.set_password('password')
        db.session.add(new_user)
        db.session.commit()
        print("User 'testuser' created successfully.")
    else:
        print("User 'testuser' already exists.")
