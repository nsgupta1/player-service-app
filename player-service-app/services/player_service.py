import sqlite3
from sqlalchemy import create_engine

class PlayerService:
    def __init__(self):
        conn = sqlite3.connect("player.db")
        self.conn = conn
        self.cursor = conn.cursor()
        self.columns = self.get_columns()
    
    def insert_player(self, player_data: dict) -> str:
        try:
            columns = [
                'playerId', 'birthYear', 'birthMonth', 'birthDay', 'birthCountry',
                'birthState', 'birthCity', 'deathYear', 'deathMonth', 'deathDay',
                'deathCountry', 'deathState', 'deathCity', 'nameFirst', 'nameLast',
                'nameGiven', 'weight', 'height', 'bats', 'throws', 'debut',
                'finalGame', 'retroID', 'bbrefID'
            ]
            
            placeholders = ','.join(['?' for _ in columns])
            values = [player_data.get(column) for column in columns]
            
            query = f'''
            INSERT INTO players ({','.join(columns)})
            VALUES ({placeholders})
            '''
            
            self.cursor.execute(query, values)
            self.conn.commit()
            return f"Player with ID {player_data['playerId']} inserted successfully"
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to insert player: {str(e)}")

    def update_player(self, player_id: str, player_data: dict) -> str:
        try:
            allowed_fields = {
                'birthYear', 'birthMonth', 'birthDay', 'birthCountry',
                'birthState', 'birthCity', 'deathYear', 'deathMonth', 'deathDay',
                'deathCountry', 'deathState', 'deathCity', 'nameFirst', 'nameLast',
                'nameGiven', 'weight', 'height', 'bats', 'throws', 'debut',
                'finalGame', 'retroID', 'bbrefID'
            }
            
            update_fields = []
            values = []
            
            for field, value in player_data.items():
                if field in allowed_fields and value is not None:
                    update_fields.append(f'{field} = ?')
                    values.append(value)
            
            if not update_fields:
                return "No valid fields provided for update"
                
            values.append(player_id)
            query = f'''
            UPDATE players 
            SET {', '.join(update_fields)}
            WHERE playerId = ?
            '''
            
            self.cursor.execute(query, values)
            self.conn.commit()
            
            if self.cursor.rowcount == 0:
                return f"No player found with ID {player_id}"
            return f"Player with ID {player_id} updated successfully"
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"Failed to update player: {str(e)}")

    def get_all_players(self):

        query = "SELECT * FROM players"
        result = self.cursor.execute(query).fetchall()
        players = []
        for row in result:
            dic = self.convert_row_to_dict(row)
            players.append(dic)

        return players

    def search_by_player(self, player_id):

        query = "SELECT * FROM players WHERE playerId='{}'".format(player_id)
        result = self.cursor.execute(query).fetchall()

        for row in result:
            dic = self.convert_row_to_dict(row)
        return dic

    def search_by_country(self, birth_country):

        query = "SELECT * FROM players WHERE birthCountry='{}'".format(birth_country)
        result = self.cursor.execute(query).fetchall()

        return result


    def convert_row_to_dict(self, row):
        dic = { self.columns[i]: row[i] for i in range(len(row)) }
        return dic


    def get_columns(self):
        self.cursor.execute("PRAGMA table_info(players)")
        columns = [column[1] for column in self.cursor.fetchall()]
        return columns
    
    
    def check_duplicate_player(self, player_data: dict) -> bool:
        try:
            with sqlite3.connect('player.db') as conn:
                cursor = conn.cursor()
                
                query = """
                SELECT EXISTS (
                    SELECT 1 FROM players 
                    WHERE nameFirst = ? COLLATE NOCASE
                    AND nameLast = ? COLLATE NOCASE
                    AND birthYear = ?
                    AND birthMonth = ?
                    AND birthDay = ?
                )
                """
                
                values = (
                    player_data['nameFirst'],
                    player_data['nameLast'],
                    player_data['birthYear'],
                    player_data['birthMonth'],
                    player_data['birthDay']
                )

                # Logging the query for debugging purposes
                print(f"Database query: {query} \n {values}")

                cursor.execute(query, values)
                exists = cursor.fetchone()[0]

                print(f"database result exists: {exists}")
                return exists == 1
            
        except sqlite3.Error as e:
            # Optionally handle specific exceptions
            print(f"Database error: {e}")
            raise

        except KeyError as e:
            print(f"Missing required player data field: {e}")
            raise ValueError(f"Missing required player data field: {e}")
        
        except Exception as e:
            print(f"unknown exception {e}")
