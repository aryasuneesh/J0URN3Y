import sqlite3
import hashlib
import json
import traceback

def get_db_connection():
    conn = sqlite3.connect('cache.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS cache
                    (key TEXT PRIMARY KEY, value TEXT)''')
    return conn

def is_valid_itinerary(data):
    print("Debug: Validating itinerary data")
    print(f"Debug: Data type: {type(data)}")
    
    if isinstance(data, str):
        try:
            data = json.loads(data)
            print("Debug: Successfully parsed JSON string")
        except json.JSONDecodeError:
            print("Debug: Failed to parse JSON string")
            return False
    
    required_keys = ['location', 'start_date', 'end_date', 'interests', 'budget', 'itinerary']
    if not all(key in data for key in required_keys):
        print("Debug: Missing required keys in itinerary object")
        return False
    
    if not isinstance(data['itinerary'], list):
        print("Debug: Itinerary is not a list")
        return False
    
    for item in data['itinerary']:
        if not all(key in item for key in ['place', 'date', 'activity', 'description']):
            print("Debug: Invalid itinerary item")
            return False
    
    print("Debug: Valid itinerary object")
    return True

def cache_api_call(func, *args, **kwargs):
    key = hashlib.md5(f"{func.__name__}_{str(args)}_{str(kwargs)}".encode()).hexdigest()
    
    print(f"Debug: Caching key: {key}")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT value FROM cache WHERE key = ?", (key,))
        result = cursor.fetchone()
        
        if result:
            print("Debug: Found result in cache")
            cached_data = json.loads(result[0])
            if is_valid_itinerary(cached_data):
                print("Debug: Returning cached data")
                return cached_data
            else:
                print("Debug: Cached data is invalid, removing from cache")
                cursor.execute("DELETE FROM cache WHERE key = ?", (key,))
                conn.commit()
        
        print("Debug: Generating new data")
        result = func(*args, **kwargs)
        
        print("Debug: Generated data:")
        print(json.dumps(result, indent=2)[:500] + "...")  # Print first 500 characters
        
        if is_valid_itinerary(result):
            print("Debug: Caching new data")
            json_result = json.dumps(result)
            cursor.execute("INSERT OR REPLACE INTO cache (key, value) VALUES (?, ?)", (key, json_result))
            conn.commit()
            print("Debug: Data cached successfully")
        else:
            print(f"Warning: Invalid itinerary data generated for key {key}. Not caching.")
        
        return result
    except Exception as e:
        print(f"Error in cache_api_call: {str(e)}")
        print(traceback.format_exc())
        return None
    finally:
        conn.close()

def clear_cache():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cache")
    conn.commit()
    conn.close()
    print("Cache cleared successfully.")

def print_cache_contents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cache")
    results = cursor.fetchall()
    conn.close()
    
    print("Cache contents:")
    for row in results:
        print(f"Key: {row[0]}")
        print(f"Value: {row[1][:100]}...")  # Print first 100 characters of the value
        print("---")