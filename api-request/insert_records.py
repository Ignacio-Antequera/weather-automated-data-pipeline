import psycopg2
from api_request import mock_fetch_data, fetch_data

def connect_to_db():
    print("Connecting to the PostgreSQL database...")
    try:
        conn = psycopg2.connect(
            dbname="db",
            user="db_user",
            password="db_password",
            host="db",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise

def create_table(conn):
    print("Creating weather_data table if not exists...")
    try:
        with conn.cursor() as cursor:
            # Create schema first
            cursor.execute("CREATE SCHEMA IF NOT EXISTS dev;")
            conn.commit()
            
            # Then create table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                    id SERIAL PRIMARY KEY,
                    city TEXT,
                    temperature FLOAT,
                    weather_description TEXT,
                    wind_speed FLOAT,
                    time TIMESTAMP,
                    inserted_at TIMESTAMP DEFAULT NOW(),
                    utc_offset TEXT
                );
            """)
            conn.commit()
            print("Table created or already exists.")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise

def insert_records(conn, data):
    print("Inserting records into weather_data table...")
    try:
        weather = data['current']
        location = data['location']
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO dev.raw_weather_data (
                    city,
                    temperature,
                    weather_description,
                    wind_speed,
                    time,
                    utc_offset
                ) VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                location['name'],
                weather['temperature'],
                weather['weather_descriptions'][0],
                weather['wind_speed'],
                location['localtime'],
                location['utc_offset']
            ))
            conn.commit()
            print("Record inserted successfully.")
    except psycopg2.Error as e:
        print(f"Failed to insert record: {e}")
        raise

def main():
    try:
        data = fetch_data()
        conn = connect_to_db()
        create_table(conn)
        insert_records(conn, data)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")
            
if __name__ == "__main__":
    main()