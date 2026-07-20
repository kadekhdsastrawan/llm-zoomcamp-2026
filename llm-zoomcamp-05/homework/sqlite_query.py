import sqlite3

def query_database(db_path):
    # 1. Connect to the database (creates the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    
    try:
        # 2. Create a cursor object to execute SQL commands
        cursor = conn.cursor()
        
        # 3. Execute your query
        cursor.execute("SELECT name, end_time - start_time FROM spans WHERE name <> 'rag'")
        
        # 4. Fetch the results
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)
            
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        
    finally:
        # 5. Always close the connection when done
        conn.close()

# Run the query
if __name__ == "__main__":
    query_database('traces.db')