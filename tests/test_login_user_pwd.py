# import hashlib
#
# input_str = "admin123"
#
# hash_obj = hashlib.sha256(input_str.encode())
#
# hex_dig = hash_obj.hexdigest()
#
# print(hex_dig)
# # 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9

import sqlite3
from bcrypt import checkpw

# Connect to the database
conn = sqlite3.connect('heatmap_app.db')
cursor = conn.cursor()

# Input credentials
username = "admin123"
password = "admin123"

# Fetch hashed password from database
cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
result = cursor.fetchone()

if result:
    stored_hashed_password = result[0]
    # Compare the hashed password
    if checkpw(password.encode(), stored_hashed_password.encode()):
        print("Login successful!")
    else:
        print("Invalid password!")
else:
    print("Invalid username!")
