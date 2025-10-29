import mysql.connector


class AuthController:
    def __init__(self,is_connected = False):
        self.is_connected = is_connected

    def isConnected(self):
        return  self.is_connected

    def connect(self,name, birthdate):
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3307,
            user="root",
            password="root",
            database="ing"
        )

        cursor = conn.cursor()

        query = """
            SELECT customer_id
            FROM customers
            WHERE name = %s 
              AND birthdate = %s;
        """

        cursor.execute(query, (name, birthdate))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            self.is_connected = True
            return result[0]  # customer_id
        return None

