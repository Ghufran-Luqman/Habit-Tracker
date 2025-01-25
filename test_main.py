from fastapi.testclient import TestClient
from main import app  # Assuming your file is named main.py
import sqlite3
import os

# Test the /submit endpoint
def test_submit():
    # Step 1: Set up a test database
    test_db = "test_tasks.db"
    conn = sqlite3.connect(test_db, check_same_thread=False)
    c = conn.cursor()
    # Create a tasks table in the test database
    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        state INTEGER DEFAULT 0
    )
    """)
    c.execute("SELECT * FROM tasks")
    print(f"tasks: {c.fetchall()}")
    conn.commit()
    conn.close()



    # Replace the database connection in the app (Monkey patching)
    def override_connect_db():
        return sqlite3.connect(test_db)
    
    app.dependency_overrides[sqlite3.connect] = override_connect_db

    # Step 2: Initialize TestClient
    client = TestClient(app)

    # Step 3: Simulate a POST request to /submit
    response = client.post("/submit", data={"inputs": "Test Task"}, allow_redirects=False)

    # Step 4: Verify the response and database
    # Check the HTTP status code is 303 (redirect)
    assert response.status_code == 303

    # Check the redirect URL
    assert response.headers["location"] == "/?alert="

    # Check the database for the inserted task
    conn = sqlite3.connect(test_db)
    c = conn.cursor()
    c.execute("SELECT name FROM tasks WHERE name = ?", ("Test Task",))
    task = c.fetchone()
    conn.close()

    # Assert that the task was added
    assert task is not None
    assert task[0] == "Test Task"

    # Clean up the test database
    os.remove(test_db)
