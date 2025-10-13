# Local PostgreSQL Setup for NOVYA LMS

This guide will help you install and configure PostgreSQL on your local system for the NOVYA LMS Django backend.

## Installation by Operating System

### Windows Installation

#### Method 1: Official Installer (Recommended)
1. **Download PostgreSQL**
   - Go to [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
   - Download the latest version (15.x or 16.x)
   - Run the installer as Administrator

2. **Installation Steps**
   - Choose installation directory (default: `C:\Program Files\PostgreSQL\15`)
   - Select components: PostgreSQL Server, pgAdmin 4, Stack Builder, Command Line Tools
   - Set superuser password (remember this password!)
   - Set port (default: 5432)
   - Set locale (default: Default locale)

3. **Post-Installation**
   - Add PostgreSQL to PATH: `C:\Program Files\PostgreSQL\15\bin`
   - Start PostgreSQL service: `net start postgresql-x64-15`

#### Method 2: Using Chocolatey
```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install PostgreSQL
choco install postgresql

# Start service
net start postgresql
```

### macOS Installation

#### Method 1: Using Homebrew (Recommended)
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Create a database
createdb $(whoami)
```

#### Method 2: Official Installer
1. Download from [https://www.postgresql.org/download/macosx/](https://www.postgresql.org/download/macosx/)
2. Run the installer package
3. Follow the installation wizard

### Linux Installation

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user
sudo -u postgres psql
```

#### CentOS/RHEL/Fedora
```bash
# Install PostgreSQL
sudo yum install postgresql-server postgresql-contrib
# or for newer versions:
sudo dnf install postgresql-server postgresql-contrib

# Initialize database
sudo postgresql-setup initdb

# Start and enable service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Database Setup

### 1. Connect to PostgreSQL

#### Windows
```cmd
# Using psql command line
psql -U postgres

# Or using pgAdmin (GUI tool)
# Open pgAdmin from Start Menu
```

#### macOS/Linux
```bash
# Switch to postgres user and connect
sudo -u postgres psql

# Or connect directly
psql -U postgres
```

### 2. Create Database and User

```sql
-- Create database
CREATE DATABASE novya_lms;

-- Create user (optional - you can use postgres user)
CREATE USER novya_user WITH PASSWORD 'your_secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE novya_lms TO novya_user;

-- Grant schema privileges
\c novya_lms
GRANT ALL ON SCHEMA public TO novya_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO novya_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO novya_user;

-- Exit psql
\q
```

### 3. Test Connection

```bash
# Test connection to your database
psql -U postgres -d novya_lms -c "SELECT version();"

# Or with custom user
psql -U novya_user -d novya_lms -c "SELECT version();"
```

## Django Configuration

### 1. Update .env File

Create or update your `.env` file in the project root:

```env
# Database Settings (Local PostgreSQL)
DB_NAME=novya_lms
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# Alternative with custom user
# DB_USER=novya_user
# DB_PASSWORD=your_secure_password
```

### 2. Install Python Dependencies

```bash
# Install psycopg2-binary (PostgreSQL adapter for Python)
pip install psycopg2-binary

# Or install all requirements
pip install -r requirements.py
```

### 3. Run Django Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate initial data
python manage.py populate_initial_data
```

## Verification

### 1. Test Database Connection

```bash
# Run the connection test script
python test_db_connection.py
```

### 2. Check Django Admin

```bash
# Start Django server
python manage.py runserver

# Visit http://localhost:8000/admin/
# Login with superuser credentials
```

### 3. Verify Tables

```sql
-- Connect to database
psql -U postgres -d novya_lms

-- List all tables
\dt

-- Check specific tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
```

## Troubleshooting

### Common Issues

#### 1. Connection Refused
```
Error: connection to server at "localhost" (127.0.0.1), port 5432 failed
```

**Solutions:**
- Check if PostgreSQL service is running
- Verify port 5432 is not blocked
- Check firewall settings

#### 2. Authentication Failed
```
Error: password authentication failed for user "postgres"
```

**Solutions:**
- Verify password in .env file
- Reset postgres password if needed
- Check pg_hba.conf configuration

#### 3. Database Does Not Exist
```
Error: database "novya_lms" does not exist
```

**Solutions:**
- Create database manually
- Check database name in .env file
- Verify user has CREATE DATABASE privileges

#### 4. Permission Denied
```
Error: permission denied for database "novya_lms"
```

**Solutions:**
- Grant proper privileges to user
- Check user roles and permissions
- Verify database ownership

### Service Management

#### Windows
```cmd
# Start PostgreSQL service
net start postgresql-x64-15

# Stop PostgreSQL service
net stop postgresql-x64-15

# Check service status
sc query postgresql-x64-15
```

#### macOS
```bash
# Start PostgreSQL
brew services start postgresql@15

# Stop PostgreSQL
brew services stop postgresql@15

# Restart PostgreSQL
brew services restart postgresql@15
```

#### Linux
```bash
# Start PostgreSQL
sudo systemctl start postgresql

# Stop PostgreSQL
sudo systemctl stop postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql

# Check status
sudo systemctl status postgresql

# Enable auto-start
sudo systemctl enable postgresql
```

## Performance Optimization

### 1. PostgreSQL Configuration

Edit `postgresql.conf` (location varies by OS):

```conf
# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB

# Connection settings
max_connections = 100

# Logging
log_statement = 'all'
log_duration = on
```

### 2. Database Maintenance

```sql
-- Analyze tables for better query planning
ANALYZE;

-- Vacuum to reclaim space
VACUUM;

-- Full vacuum and analyze
VACUUM ANALYZE;
```

## Backup and Restore

### Backup Database
```bash
# Create backup
pg_dump -U postgres -h localhost novya_lms > novya_lms_backup.sql

# Compressed backup
pg_dump -U postgres -h localhost -Fc novya_lms > novya_lms_backup.dump
```

### Restore Database
```bash
# Restore from SQL file
psql -U postgres -h localhost -d novya_lms < novya_lms_backup.sql

# Restore from compressed dump
pg_restore -U postgres -h localhost -d novya_lms novya_lms_backup.dump
```

## Security Best Practices

1. **Change Default Password**: Always change the default postgres password
2. **Create Application User**: Don't use postgres user for applications
3. **Limit Connections**: Configure max_connections appropriately
4. **Enable SSL**: Use SSL connections in production
5. **Regular Updates**: Keep PostgreSQL updated
6. **Backup Regularly**: Implement automated backup strategy

## Next Steps

After successful PostgreSQL setup:

1. **Test Connection**: Run `python test_db_connection.py`
2. **Run Migrations**: `python manage.py migrate`
3. **Create Superuser**: `python manage.py createsuperuser`
4. **Populate Data**: `python manage.py populate_initial_data`
5. **Start Server**: `python manage.py runserver`
6. **Access Admin**: Visit http://localhost:8000/admin/

Your Django backend is now ready to use PostgreSQL on your local system! 🎉
