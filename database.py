import psycopg2 as pg
from dotenv import load_dotenv
import os

load_dotenv()  

hostname = os.getenv("HOSTNAME")
database = os.getenv("DATABASE")
username = os.getenv("USERNAME")
pwd = os.getenv("DB_PASSWORD")
port_id = os.getenv("PORT_ID")


def get_db_connection():
    try:
        conn = pg.connect(
            dbname=database,
            user=username,
            password=pwd,
            host=hostname,
            port=port_id,
        )
        return conn
    except Exception as e:
        print("Connection failed")
        print(e)
        return None

def create_users_table():
    conn = get_db_connection()
    if conn is None:
        print("Unable to connect to database. Table not created.")
        return

    create_table_query = """
                CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                date_of_birth DATE,
                address TEXT,
                gender VARCHAR(10),
                pincode INTEGER,  
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
    
    try:
        cur = conn.cursor()
        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        print("Table 'users' created successfully or already exists.")
    except Exception as e:
        print("Failed to create table.")
        print(e)
    finally:
        conn.close()
        
def create_user_images():
    conn = get_db_connection()
    if conn is None:
        print("Unable to connect to database. Table not created.")
        return 
    
    user_images_query = """
        CREATE TABLE IF NOT EXISTS user_images (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            style VARCHAR(50),
            original_image_url TEXT,
            processed_image_url TEXT, 
            payment_status VARCHAR(20) DEFAULT 'pending',
            download_status VARCHAR(20) DEFAULT 'not_downloaded',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """
    
    try:
        cur = conn.cursor()
        cur.execute(user_images_query)
        conn.commit()
        cur.close()
        print("Table 'user_images' created successfully or already exists.")
    except Exception as e:
        print("Failed to create table.")
        print(e)
    finally:
        conn.close()
    


create_users_table()
create_user_images()
