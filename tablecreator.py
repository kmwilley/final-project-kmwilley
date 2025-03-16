import mysql.connector
from creds import Creds

# Establish a connection to SQL database using creds
con = mysql.connector.connect(
    host=Creds.hostname,
    user=Creds.username,
    password=Creds.password,
    database=Creds.database
)

cursor = con.cursor()

# SQL query to create the 'carshowroom' table if it does not already exist
create_table_query = """
CREATE TABLE IF NOT EXISTS carshowroom(
    id INT AUTO_INCREMENT PRIMARY KEY,
    carname VARCHAR(100) NOT NULL,
    carmodel VARCHAR(50) NOT NULL,
    carcategory VARCHAR(50),
    quantity INT CHECK (quantity >= 0),
    status ENUM('available', 'sold', 'reserved') NOT NULL
);
"""

cursor.execute(create_table_query)

print("Table 'carshowroom' created successfully.") # Confirmation message

cursor.close()