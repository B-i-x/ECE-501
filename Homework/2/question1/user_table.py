import sqlite3

def create_and_populate_user_table(con: sqlite3.Connection):
    """
    Create and populate a users table with sample data.
    Generates users matching the UserIDs found in the ratings table.
    """
    cur = con.cursor()
    
    # Create users table
    cur.execute("""
        DROP TABLE IF EXISTS users;
    """)
    
    cur.execute("""
        CREATE TABLE users (
            userId INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL
        );
    """)
    
    # Get unique user IDs from ratings table
    cur.execute("SELECT DISTINCT userId FROM ratings ORDER BY userId")
    user_ids = [row[0] for row in cur.fetchall()]
    
    # Sample data for generating users
    first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", 
                   "Ivy", "Jack", "Kate", "Leo", "Maya", "Noah", "Olivia", "Paul", 
                   "Quinn", "Rose", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xavier", "Yara", "Zoe"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", 
                  "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", 
                  "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
    genders = ["M", "F", "Other"]
    
    # Generate sample users
    import random
    random.seed(42)  # For reproducibility
    
    users_to_insert = []
    for user_id in user_ids:
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(15, 65)  # Mix of ages including under 25
        gender = random.choice(genders)
        users_to_insert.append((user_id, name, age, gender))
    
    # Insert users into table
    con.executemany(
        "INSERT INTO users (userId, name, age, gender) VALUES (?, ?, ?, ?)",
        users_to_insert
    )
    con.commit()
    
    print(f"Created users table with {len(users_to_insert)} sample users")