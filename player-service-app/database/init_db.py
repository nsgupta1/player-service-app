import os
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

def create_player_index():
    try:
        conn = sqlite3.connect('player.db')
        cursor = conn.cursor()
        
        # Create composite index on player identifying fields
        query = """
        CREATE INDEX IF NOT EXISTS idx_player_identity
        ON players (nameFirst, nameLast, birthYear, birthMonth, birthDay);
        """
        
        cursor.execute(query)
        conn.commit()
        print("Player index created successfully")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        if conn:
            conn.close()

def initialize_database():
    db_file = 'player.db'
    csv_file = 'data/Player.csv'

    # Check if the database file exists
    if not os.path.exists(db_file):
        # Load CSV file into pandas DataFrame
        df = pd.read_csv(csv_file)

        # Create SQLite database and write DataFrame to it
        engine = create_engine(f'sqlite:///{db_file}', echo=False)
        df.to_sql('players', con=engine, if_exists='replace', index=False)
        create_player_index()
        print("Database created and initialized from CSV.")
    else:
        print("Database already exists. Skipping initialization.")