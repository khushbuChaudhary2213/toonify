import psycopg2 as pg

hostname = 'localhost'
database = 'toonify'
username = 'postgres'
pwd = 'Khushi@4321'
port_id = 5432

def get_db_connection():
    try:
        conn = pg.connect(
            dbname=database,
            user=username,
            password=pwd,
            host=hostname,
            port=port_id,
        )
        # print("Connected to PostgreSQL successfully")
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
        
create_users_table()
