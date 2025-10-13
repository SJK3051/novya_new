#!/usr/bin/env python
"""
Database Sync Script for NOVYA LMS
This script helps sync Django models with your existing PostgreSQL database schema.
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

def print_header():
    """Print sync header"""
    print("🔄 NOVYA LMS Database Sync")
    print("=" * 50)

def check_database_connection():
    """Check database connection"""
    print("🔍 Checking database connection...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Connected to: {version}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_existing_tables():
    """Check existing tables in database"""
    print("\n🔍 Checking existing tables...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            if tables:
                print("✅ Found existing tables:")
                for table in tables:
                    print(f"  - {table[0]}")
                return True
            else:
                print("⚠️ No tables found in database")
                return False
                
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def create_missing_tables():
    """Create missing Django tables"""
    print("\n🔄 Creating missing Django tables...")
    
    try:
        # Run makemigrations
        print("Creating migration files...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        # Run migrate with --fake-initial to avoid conflicts
        print("Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--fake-initial'])
        
        print("✅ Django tables created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create Django tables: {e}")
        return False

def verify_table_mapping():
    """Verify table mapping between Django models and existing tables"""
    print("\n🔍 Verifying table mapping...")
    
    # Expected table mappings
    expected_tables = {
        'users': 'authentication.User',
        'class': 'authentication.Class',
        'parent': 'authentication.Parent',
        'student': 'authentication.Student',
        'course': 'courses.Course',
        'topic': 'courses.Topic',
        'pdf_files': 'courses.PDFFiles',
        'videofiles': 'courses.VideoFiles',
        'assignment': 'progress.Assignment',
        'assignmentquestion': 'progress.AssignmentQuestion',
        'assignmentsubmission': 'progress.AssignmentSubmission',
        'assignmentanswer': 'progress.AssignmentAnswer',
        'quiz': 'quizzes.Quiz',
        'quizattempt': 'quizzes.QuizAttempt',
        'mocktest': 'quizzes.MockTest',
        'careerperformance': 'progress.CareerPerformance',
        'mentorshipticket': 'progress.MentorshipTicket',
        'review': 'notifications.Review',
        'rating': 'notifications.Rating',
        'report': 'notifications.Report',
    }
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """)
            existing_tables = [table[0] for table in cursor.fetchall()]
            
            print("✅ Table mapping verification:")
            for table_name, model_name in expected_tables.items():
                if table_name in existing_tables:
                    print(f"  ✅ {table_name} -> {model_name}")
                else:
                    print(f"  ⚠️ {table_name} -> {model_name} (not found)")
            
            return True
            
    except Exception as e:
        print(f"❌ Error verifying table mapping: {e}")
        return False

def create_superuser():
    """Create Django superuser"""
    print("\n👤 Creating Django superuser...")
    
    try:
        execute_from_command_line(['manage.py', 'createsuperuser'])
        print("✅ Superuser created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create superuser: {e}")
        return False

def populate_initial_data():
    """Populate initial data"""
    print("\n📊 Populating initial data...")
    
    try:
        execute_from_command_line(['manage.py', 'populate_initial_data'])
        print("✅ Initial data populated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to populate initial data: {e}")
        return False

def main():
    """Main sync function"""
    print_header()
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Please run this script from the Django project root directory")
        sys.exit(1)
    
    # Check database connection
    if not check_database_connection():
        sys.exit(1)
    
    # Check existing tables
    if not check_existing_tables():
        print("❌ No existing tables found. Please check your database connection.")
        sys.exit(1)
    
    # Create missing Django tables
    if not create_missing_tables():
        sys.exit(1)
    
    # Verify table mapping
    if not verify_table_mapping():
        sys.exit(1)
    
    # Create superuser
    create_superuser_choice = input("\n❓ Do you want to create a Django superuser? (y/n): ").lower().strip()
    if create_superuser_choice == 'y':
        if not create_superuser():
            sys.exit(1)
    
    # Populate initial data
    populate_choice = input("\n❓ Do you want to populate initial data? (y/n): ").lower().strip()
    if populate_choice == 'y':
        if not populate_initial_data():
            sys.exit(1)
    
    print("\n🎉 Database sync completed successfully!")
    print("\n📋 Next steps:")
    print("1. Test database connection: python test_db_connection.py")
    print("2. Start Django server: python manage.py runserver")
    print("3. Access Django admin: http://localhost:8000/admin/")
    print("4. Test API endpoints: http://localhost:8000/api/")
    print("\n🌐 Your existing database schema is now integrated with Django!")

if __name__ == "__main__":
    main()
