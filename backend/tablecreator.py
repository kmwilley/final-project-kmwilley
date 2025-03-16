import mysql.connector
from creds import Creds


def create_tables():
    try:
        # Establish a connection to SQL database using creds
        con = mysql.connector.connect(
            host=Creds.hostname,
            user=Creds.username,
            password=Creds.password,
            database=Creds.database
        )
        cursor = con.cursor()

        # SQL query to create books table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                genre VARCHAR(100),
                status ENUM('available', 'unavailable') NOT NULL DEFAULT 'available'
            );
        """)

        # SQL query to create customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                firstname VARCHAR(100) NOT NULL,
                lastname VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                passwordhash VARCHAR(255) NOT NULL
            );
        """)

        # SQL query to create borrowingrecords table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrowingrecords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                bookid INT NOT NULL,
                customerid INT NOT NULL,
                borrowdate DATE NOT NULL,
                returndate DATE DEFAULT NULL,
                late_fee DECIMAL(5,2) DEFAULT 0,
                FOREIGN KEY (bookid) REFERENCES books(id) ON DELETE CASCADE,
                FOREIGN KEY (customerid) REFERENCES customers(id) ON DELETE CASCADE
            );
        """)

        # Commits changes and closes connection
        con.commit()
        cursor.close()
        con.close()

        print("Tables created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    create_tables()
    
                                
    