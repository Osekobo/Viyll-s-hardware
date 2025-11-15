from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()












# database setup script
# setup_database.py

import psycopg2
from decouple import config

def setup_database():
    # Database connection parameters
    db_params = {
        'host': 'localhost',
        'database': 'postgres',  # Connect to default database first
        'user': 'postgres',
        'password': config('DB_PASSWORD', default='password')
    }
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE kione_hardware;")
        print("Database 'kione_hardware' created successfully")
        
        # Create user (optional)
        try:
            cursor.execute("CREATE USER kione_user WITH PASSWORD 'kione_password';")
            cursor.execute("GRANT ALL PRIVILEGES ON DATABASE kione_hardware TO kione_user;")
            print("User 'kione_user' created successfully")
        except Exception as e:
            print(f"User might already exist: {e}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if _name_ == "_main_":
    setup_database()