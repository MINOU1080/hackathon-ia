import mysql.connector


class AuthController:
    def __init__(self,is_connected,name,birthdate):
        self.is_connected = is_connected
        self.name = name
        self.birthdate = birthdate


    def isConnected(self):
        return  self.is_connected


    def connect(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ing"
        )

        cursor = conn.cursor()

        query = """
            SELECT customer_id
            FROM customers
            WHERE name = %s 
              AND birthdate = %s;
        """

        cursor.execute(query, (self.name, self.birthdate))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            self.is_connected = True
            return result[0]  # customer_id
        return None

