import psycopg2

try:
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        database='NOVYA',
        user='postgres',
        password='srinu'
    )
    
    cursor = conn.cursor()
    
    # Get all columns in users table
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'users' AND table_schema = 'public'
        ORDER BY ordinal_position;
    """)
    
    columns = cursor.fetchall()
    
    print("=== ALL COLUMNS IN USERS TABLE ===")
    for col in columns:
        print(f"- {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
