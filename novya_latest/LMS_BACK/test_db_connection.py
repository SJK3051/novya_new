#!/usr/bin/env python
"""
Database connection test script for NOVYA LMS
This script tests the PostgreSQL database connection and displays connection details.
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

from django.conf import settings
from django.db import connection, connections
from django.core.management import execute_from_command_line

def test_database_connection():
    """Test database connection and display connection details"""
    print("🔍 Testing Database Connection")
    print("=" * 50)
    
    try:
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            
            cursor.execute("SELECT current_user;")
            db_user = cursor.fetchone()[0]
            
            cursor.execute("SELECT inet_server_addr();")
            db_host = cursor.fetchone()[0] or 'localhost'
            
            cursor.execute("SELECT inet_server_port();")
            db_port = cursor.fetchone()[0]
        
        print("✅ Database connection successful!")
        print(f"📊 Database: {db_name}")
        print(f"👤 User: {db_user}")
        print(f"🌐 Host: {db_host}")
        print(f"🔌 Port: {db_port}")
        print(f"📝 PostgreSQL Version: {version}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Check if PostgreSQL is running")
        print("2. Verify database credentials in .env file")
        print("3. Ensure database exists")
        print("4. Check network connectivity")
        return False

def check_django_settings():
    """Check Django database settings"""
    print("\n⚙️ Django Database Settings")
    print("=" * 50)
    
    db_config = settings.DATABASES['default']
    
    print(f"Engine: {db_config['ENGINE']}")
    print(f"Name: {db_config['NAME']}")
    print(f"User: {db_config['USER']}")
    print(f"Host: {db_config['HOST']}")
    print(f"Port: {db_config['PORT']}")
    print(f"Password: {'*' * len(db_config['PASSWORD']) if db_config['PASSWORD'] else 'Not set'}")

def check_migrations():
    """Check migration status"""
    print("\n📋 Migration Status")
    print("=" * 50)
    
    try:
        from django.db.migrations.executor import MigrationExecutor
        from django.db import connection
        
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print("⚠️ Pending migrations:")
            for migration, backwards in plan:
                print(f"  - {migration}")
        else:
            print("✅ All migrations are up to date")
            
    except Exception as e:
        print(f"❌ Error checking migrations: {e}")

def check_tables():
    """Check if Django tables exist"""
    print("\n🗄️ Database Tables")
    print("=" * 50)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE '%auth%' OR table_name LIKE '%course%' OR table_name LIKE '%quiz%'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            if tables:
                print("✅ Django tables found:")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("⚠️ No Django tables found. Run migrations first.")
                
    except Exception as e:
        print(f"❌ Error checking tables: {e}")

def main():
    """Main function"""
    print("🚀 NOVYA LMS Database Connection Test")
    print("=" * 60)
    
    # Check Django settings
    check_django_settings()
    
    # Test database connection
    if test_database_connection():
        # Check migrations
        check_migrations()
        
        # Check tables
        check_tables()
        
        print("\n🎉 Database setup looks good!")
        print("\n📋 Next steps:")
        print("1. Run migrations if needed: python manage.py migrate")
        print("2. Create superuser: python manage.py createsuperuser")
        print("3. Populate data: python manage.py populate_initial_data")
        print("4. Start server: python manage.py runserver")
    else:
        print("\n❌ Database setup needs attention.")
        print("Please check the DATABASE_SETUP.md file for detailed instructions.")

if __name__ == "__main__":
    main()
