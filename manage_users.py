"""
User management utility script for the Fraud Detection System.
Helps with viewing, creating, and deleting users.
"""
from database import SessionLocal
from db_models import User
from auth import get_password_hash
from datetime import datetime
import sys


def list_users():
    """List all users in the database."""
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"\n{'='*80}")
        print(f"Total users in database: {len(users)}")
        print(f"{'='*80}\n")
        
        if users:
            for i, user in enumerate(users, 1):
                print(f"{i}. Username: {user.username}")
                print(f"   Email: {user.email}")
                print(f"   Role: {user.role}")
                print(f"   Created: {user.created_at}")
                print(f"   ID: {user.id}")
                print()
        else:
            print("No users found in database.\n")
    finally:
        db.close()


def delete_user_by_username(username):
    """Delete a user by username."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            db.delete(user)
            db.commit()
            print(f"✓ User '{username}' deleted successfully.")
        else:
            print(f"✗ User '{username}' not found.")
    finally:
        db.close()


def delete_user_by_email(email):
    """Delete a user by email."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            username = user.username
            db.delete(user)
            db.commit()
            print(f"✓ User with email '{email}' (username: {username}) deleted successfully.")
        else:
            print(f"✗ User with email '{email}' not found.")
    finally:
        db.close()


def create_admin_user(username, email, password):
    """Create an admin user."""
    db = SessionLocal()
    try:
        # Check if username exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"✗ Username '{username}' already exists.")
            return
        
        # Check if email exists
        existing_email = db.query(User).filter(User.email == email).first()
        if existing_email:
            print(f"✗ Email '{email}' already exists.")
            return
        
        # Create admin user
        hashed_password = get_password_hash(password)
        admin = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role="admin",
            created_at=datetime.now()
        )
        db.add(admin)
        db.commit()
        print(f"✓ Admin user '{username}' created successfully.")
    finally:
        db.close()


def clear_all_users():
    """Delete all users from the database (use with caution!)."""
    db = SessionLocal()
    try:
        count = db.query(User).count()
        if count == 0:
            print("No users to delete.")
            return
        
        confirm = input(f"⚠️  Are you sure you want to delete ALL {count} users? (yes/no): ")
        if confirm.lower() == 'yes':
            db.query(User).delete()
            db.commit()
            print(f"✓ All {count} users deleted successfully.")
        else:
            print("Operation cancelled.")
    finally:
        db.close()


def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 2:
        print("\nUser Management Utility")
        print("=" * 80)
        print("\nUsage:")
        print("  python manage_users.py list                          - List all users")
        print("  python manage_users.py delete <username>             - Delete user by username")
        print("  python manage_users.py delete-email <email>          - Delete user by email")
        print("  python manage_users.py create-admin <user> <email> <pass> - Create admin user")
        print("  python manage_users.py clear-all                     - Delete all users")
        print("\nExamples:")
        print("  python manage_users.py list")
        print("  python manage_users.py delete testuser")
        print("  python manage_users.py delete-email test@example.com")
        print("  python manage_users.py create-admin admin admin@example.com Admin@123")
        print("  python manage_users.py clear-all")
        print()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_users()
    
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("✗ Please provide username to delete.")
            print("Usage: python manage_users.py delete <username>")
        else:
            delete_user_by_username(sys.argv[2])
    
    elif command == 'delete-email':
        if len(sys.argv) < 3:
            print("✗ Please provide email to delete.")
            print("Usage: python manage_users.py delete-email <email>")
        else:
            delete_user_by_email(sys.argv[2])
    
    elif command == 'create-admin':
        if len(sys.argv) < 5:
            print("✗ Please provide username, email, and password.")
            print("Usage: python manage_users.py create-admin <username> <email> <password>")
        else:
            create_admin_user(sys.argv[2], sys.argv[3], sys.argv[4])
    
    elif command == 'clear-all':
        clear_all_users()
    
    else:
        print(f"✗ Unknown command: {command}")
        print("Run 'python manage_users.py' without arguments to see usage.")


if __name__ == "__main__":
    main()
