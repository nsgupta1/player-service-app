from typing import Optional
import datetime

def validate_player_data(data: dict) -> Optional[str]:
    """Validate player data types and constraints"""
    try:
        # Integer validations
        int_fields = ['birthYear', 'birthMonth', 'birthDay', 'deathYear', 
                      'deathMonth', 'deathDay', 'weight', 'height']
        for field in int_fields:
            if field in data and data[field] is not None:
                if not isinstance(data[field], int):
                    return f"{field} must be an integer"
                
        # String validations
        str_fields = ['nameFirst', 'nameLast', 'nameGiven', 'birthCountry', 
                      'birthState', 'birthCity', 'deathCountry', 'deathState', 
                      'deathCity', 'bats', 'throws', 'retroID', 'bbrefID']
        for field in str_fields:
            if field in data and data[field] is not None:
                if not isinstance(data[field], str):
                    return f"{field} must be a string"
                
        # Specific validations
        if 'bats' in data and data['bats'] not in ['R', 'L', 'B', None]:
            return "bats must be 'R', 'L', or 'B'"
            
        if 'throws' in data and data['throws'] not in ['R', 'L', None]:
            return "throws must be 'R' or 'L'"
            
        # Date format validations
        date_fields = ['debut', 'finalGame']
        for field in date_fields:
            if field in data and data[field] is not None:
                try:
                    datetime.datetime.strptime(data[field], '%Y-%m-%d')
                except ValueError:
                    return f"{field} must be in YYYY-MM-DD format"
                    
        return None
        
    except Exception as e:
        return str(e)