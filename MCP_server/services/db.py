import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self, db_path: str = "bookings.db"):
        # db_path arg kept for backward compatibility signature, but we use env vars for Supabase
        self.user = os.getenv("user")
        self.password = os.getenv("password")
        self.host = os.getenv("host")
        self.port = os.getenv("port")
        self.dbname = os.getenv("dbname")
        self.init_db()
    
    def init_db(self):
        # Remote DB initialization check
        try:
            conn = self.get_connection()
            conn.close()
            print("Database connection successfully established")
        except Exception as e:
            print(f"Warning: Could not connect to database: {e}")
    
    def get_connection(self):
        # get a database connection
        conn = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            cursor_factory=RealDictCursor
        )
        return conn
     
     # following two function are not essestinal but jsut ease to manuualy esecute in serveices/*.py file.
    def execute_query(self, query: str, params: tuple = ()):
        # Execute a SELECT query and return results
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        finally:
            conn.close()
    
    def execute_update(self, query: str, params: tuple = ()):
        # Execute INSERT/UPDATE/DELETE
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            
            # Postgre migration: 'lastrowid' is not supported directly.
            # If the query has 'RETURNING id', we fetch it.
            lastrowid = None
            if cursor.description:
                res = cursor.fetchone()
                if res:
                    # Get first value from dict
                    lastrowid = list(res.values())[0]
            
            conn.close()
            return lastrowid
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e

db = Database()