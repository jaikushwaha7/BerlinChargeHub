## Login is HAsh encrypted

## Creating a Secure User for the Application

To create a new user securely, follow these steps:

### 1. Open the environment terminal and access the database:
```bash
sqlite3 heatmap_app.db
```

### 2. Generate a securely hashed password:
Use the following Python script to create a hashed password:

```python
from bcrypt import hashpw, gensalt

# Replace 'yourpassword' with the desired password
password = "yourpassword"
hashed_password = hashpw(password.encode(), gensalt()).decode()

print("Hashed password:", hashed_password)
```

Replace the placeholder `HASHED_PASSWORD_HERE` in the next query with the output.

### 3. Add the new user to the database:
Run the following SQL query to add the new user. Replace `HASHED_PASSWORD_HERE` with the hashed password generated in Step 2:

```sql
INSERT INTO users (username, password_hash, created_at) 
VALUES ('admin2', 'admin2', datetime('now'));
```

### 4. Verify the new user:
To confirm that the user was added successfully, run the following SQL query:

```sql
SELECT * FROM users;
```