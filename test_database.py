import os
import psycopg2
from urllib.parse import urlparse

# Load environment variables if needed
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:XkiLdGTHPnTTPIkCWluLkvQbHsVZeSij@junction.proxy.rlwy.net:18856/railway')

# Parse the database URL
url = urlparse(DATABASE_URL)
print(url.hostname)
try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=url.path[1:],  # Skip the leading '/'
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
    )
    print("Database connection successful!")
    
    # Optionally, execute a simple query
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1;")
        print("Query executed successfully:", cursor.fetchone())
    
except Exception as e:
    print("Error connecting to the database:", e)
finally:
    if 'conn' in locals():
        conn.close()
