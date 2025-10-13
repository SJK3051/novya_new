#!/usr/bin/env python
"""
Local PostgreSQL Setup Script for NOVYA LMS
This script helps set up PostgreSQL on your local system without Docker.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print setup header"""
    print("🐘 NOVYA LMS Local PostgreSQL Setup")
    print("=" * 50)

def detect_os():
    """Detect operating system"""
    system = platform.system().lower()
    print(f"🖥️ Detected OS: {system}")
    return system

def check_postgresql_installation():
    """Check if PostgreSQL is installed"""
    print("\n🔍 Checking PostgreSQL installation...")
    
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ PostgreSQL is installed: {version}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ PostgreSQL is not installed")
    return False

def check_postgresql_service():
    """Check if PostgreSQL service is running"""
    print("\n🔍 Checking PostgreSQL service...")
    
    system = platform.system().lower()
    
    if system == 'windows':
        try:
            result = subprocess.run(['sc', 'query', 'postgresql'], capture_output=True, text=True)
            if 'RUNNING' in result.stdout:
                print("✅ PostgreSQL service is running")
                return True
            else:
                print("❌ PostgreSQL service is not running")
                return False
        except:
            print("❌ Could not check PostgreSQL service status")
            return False
    
    elif system == 'darwin':  # macOS
        try:
            result = subprocess.run(['brew', 'services', 'list'], capture_output=True, text=True)
            if 'postgresql' in result.stdout and 'started' in result.stdout:
                print("✅ PostgreSQL service is running")
                return True
            else:
                print("❌ PostgreSQL service is not running")
                return False
        except:
            print("❌ Could not check PostgreSQL service status")
            return False
    
    else:  # Linux
        try:
            result = subprocess.run(['systemctl', 'is-active', 'postgresql'], capture_output=True, text=True)
            if result.stdout.strip() == 'active':
                print("✅ PostgreSQL service is running")
                return True
            else:
                print("❌ PostgreSQL service is not running")
                return False
        except:
            print("❌ Could not check PostgreSQL service status")
            return False

def install_postgresql_instructions():
    """Show PostgreSQL installation instructions"""
    system = platform.system().lower()
    
    print("\n📋 PostgreSQL Installation Instructions:")
    print("=" * 50)
    
    if system == 'windows':
        print("🪟 Windows Installation:")
        print("1. Download PostgreSQL from: https://www.postgresql.org/download/windows/")
        print("2. Run the installer as Administrator")
        print("3. Remember the password you set for the 'postgres' user")
        print("4. Make sure to install 'Command Line Tools'")
        print("5. Add PostgreSQL to your PATH: C:\\Program Files\\PostgreSQL\\15\\bin")
        print("\nAlternative (Chocolatey):")
        print("choco install postgresql")
    
    elif system == 'darwin':  # macOS
        print("🍎 macOS Installation:")
        print("1. Install Homebrew (if not installed):")
        print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        print("2. Install PostgreSQL:")
        print("   brew install postgresql@15")
        print("3. Start PostgreSQL:")
        print("   brew services start postgresql@15")
        print("4. Create a database:")
        print("   createdb $(whoami)")
    
    else:  # Linux
        print("🐧 Linux Installation:")
        print("Ubuntu/Debian:")
        print("  sudo apt update")
        print("  sudo apt install postgresql postgresql-contrib")
        print("  sudo systemctl start postgresql")
        print("  sudo systemctl enable postgresql")
        print("\nCentOS/RHEL/Fedora:")
        print("  sudo yum install postgresql-server postgresql-contrib")
        print("  sudo postgresql-setup initdb")
        print("  sudo systemctl start postgresql")
        print("  sudo systemctl enable postgresql")

def start_postgresql_service():
    """Start PostgreSQL service"""
    print("\n🔄 Starting PostgreSQL service...")
    
    system = platform.system().lower()
    
    try:
        if system == 'windows':
            subprocess.run(['net', 'start', 'postgresql'], check=True)
        elif system == 'darwin':  # macOS
            subprocess.run(['brew', 'services', 'start', 'postgresql@15'], check=True)
        else:  # Linux
            subprocess.run(['sudo', 'systemctl', 'start', 'postgresql'], check=True)
        
        print("✅ PostgreSQL service started successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start PostgreSQL service: {e}")
        return False

def test_postgresql_connection():
    """Test PostgreSQL connection"""
    print("\n🔍 Testing PostgreSQL connection...")
    
    try:
        result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres', '-c', 'SELECT version();'
        ], capture_output=True, text=True, input='\n')
        
        if result.returncode == 0:
            print("✅ PostgreSQL connection successful")
            return True
        else:
            print("❌ PostgreSQL connection failed")
            print("Error:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def create_database():
    """Create the novya_lms database"""
    print("\n🗄️ Creating database...")
    
    try:
        # Check if database exists
        check_result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres', '-tAc', 
            "SELECT 1 FROM pg_database WHERE datname='novya_lms'"
        ], capture_output=True, text=True)
        
        if check_result.stdout.strip() == '1':
            print("✅ Database 'novya_lms' already exists")
            return True
        
        # Create database
        create_result = subprocess.run([
            'psql', '-U', 'postgres', '-d', 'postgres', '-c', 
            'CREATE DATABASE novya_lms;'
        ], capture_output=True, text=True)
        
        if create_result.returncode == 0:
            print("✅ Database 'novya_lms' created successfully")
            return True
        else:
            print("❌ Failed to create database")
            print("Error:", create_result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

def create_env_file():
    """Create .env file with PostgreSQL configuration"""
    print("\n📝 Creating .env file...")
    
    env_content = """# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Settings (Local PostgreSQL)
DB_NAME=novya_lms
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Email Settings (for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Celery Settings
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Redis Settings
REDIS_URL=redis://localhost:6379/0

# Media and Static Files
MEDIA_ROOT=media/
STATIC_ROOT=staticfiles/

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CORS_ALLOW_CREDENTIALS=True

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/django.log
"""
    
    env_file = Path('.env')
    if env_file.exists():
        print("⚠️ .env file already exists. Skipping creation.")
        return True
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("⚠️ Please update the DB_PASSWORD in .env file with your PostgreSQL password")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def run_django_setup():
    """Run Django setup commands"""
    print("\n🐍 Running Django setup...")
    
    commands = [
        ("python manage.py makemigrations", "Creating migration files"),
        ("python manage.py migrate", "Applying migrations"),
    ]
    
    for command, description in commands:
        print(f"🔄 {description}...")
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"✅ {description} completed")
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e}")
            return False
    
    return True

def main():
    """Main setup function"""
    print_header()
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ Please run this script from the Django project root directory")
        sys.exit(1)
    
    # Detect OS
    system = detect_os()
    
    # Check PostgreSQL installation
    if not check_postgresql_installation():
        install_postgresql_instructions()
        print("\n❌ Please install PostgreSQL first, then run this script again.")
        sys.exit(1)
    
    # Check PostgreSQL service
    if not check_postgresql_service():
        print("\n❓ PostgreSQL service is not running. Do you want to start it? (y/n): ", end="")
        choice = input().lower().strip()
        if choice == 'y':
            if not start_postgresql_service():
                print("❌ Failed to start PostgreSQL service")
                sys.exit(1)
        else:
            print("❌ PostgreSQL service must be running to continue")
            sys.exit(1)
    
    # Test connection
    if not test_postgresql_connection():
        print("\n❌ Cannot connect to PostgreSQL. Please check:")
        print("1. PostgreSQL service is running")
        print("2. Password is correct")
        print("3. User 'postgres' exists")
        sys.exit(1)
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Run Django setup
    if not run_django_setup():
        sys.exit(1)
    
    print("\n🎉 Local PostgreSQL setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update DB_PASSWORD in .env file with your PostgreSQL password")
    print("2. Create superuser: python manage.py createsuperuser")
    print("3. Populate data: python manage.py populate_initial_data")
    print("4. Test connection: python test_db_connection.py")
    print("5. Start server: python manage.py runserver")
    print("\n🌐 Access points:")
    print("- Django Admin: http://localhost:8000/admin/")
    print("- API: http://localhost:8000/api/")

if __name__ == "__main__":
    main()
