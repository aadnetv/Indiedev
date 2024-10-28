from app import app, db

def recreate_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database tables recreated successfully!")

if __name__ == "__main__":
    recreate_database()
