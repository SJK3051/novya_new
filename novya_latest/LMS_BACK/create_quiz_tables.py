#!/usr/bin/env python
"""
Script to create quiz tables according to the provided schema
"""
import os
import django
import psycopg2
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def create_quiz_tables():
    """Create quiz tables using the provided schema"""
    
    # Read the SQL file
    with open('create_quiz_tables.sql', 'r') as f:
        sql_commands = f.read()
    
    # Get database connection info from Django settings
    db_config = settings.DATABASES['default']
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=db_config['HOST'],
            database=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            port=db_config['PORT']
        )
        
        cursor = conn.cursor()
        
        # Execute the SQL commands
        cursor.execute(sql_commands)
        conn.commit()
        
        print("✅ Quiz tables created successfully!")
        
        # Verify tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('quiz', 'quiz_question', 'quiz_attempt', 'quiz_answer', 'mock_test', 'mock_test_question', 'mock_test_attempt')
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print("\n📋 Created tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error creating tables: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_quiz_tables()
