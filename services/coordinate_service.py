import psycopg2
from datetime import datetime
import os
from models.coordinate_model import Coordinate

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Create a new instance of DatabaseManager if it doesn't exist."""
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the DatabaseManager instance."""
        if self._initialized:
            return
        self.host = "db"
        self.port = 5432
        self.database = "coords"
        self.user = "micro_user"
        self.password = "password"
        self.connection = None
        self.cursor = None
        self._initialized = True
        self.connect()

    def __del__(self):
        """Disconnect from the database when the instance is deleted."""
        self.disconnect()

    def connect(self):
        """Connect to the PostgreSQL database."""
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        """Disconnect from the PostgreSQL database."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    @classmethod
    def create_db(cls):
        """Create the database using an external script."""
        os.system("./services/create_db.sh")

    @classmethod
    def allow_users(cls):
        """Allow users using an external script."""
        os.system("./services/allow_users.sh")

    def insert_data(self, coord_entry: Coordinate) -> bool:
        """
        Insert data into the coord table.

        Parameters:
        - coord_entry (Coordinate): An instance of the Coordinate class containing data to be inserted.

        Returns:
        - bool: True if the insertion is successful, False otherwise.
        """
        try:
            lat, lon = coord_entry.latitude, coord_entry.longitude
            timestamp = coord_entry.time
            ip = coord_entry.ip

            self.cursor.execute(
                "INSERT INTO coord (ip, time, latitude, longitude) VALUES (%s, %s, %s, %s);",
                (ip, timestamp, lat, lon),
            )

            self.connection.commit()
            result = True

        except Exception as e:
            self.connection.rollback()
            print(f"Erreur lors de l'insertion des données : {e}")
            result = False

        return result

    def readAll(self) -> dict:
        """
        Read all data from the coord table.

        Returns:
        - dict: A dictionary containing Coordinate instances with coord_id as keys.
        """
        result_dict = {}

        try:
            self.cursor.execute("SELECT * FROM coord;")
            rows = self.cursor.fetchall()

            for row in rows:
                coord_id, ip, timestamp, latitude, longitude = row
                result_dict[coord_id] = Coordinate(ip, timestamp, latitude, longitude)

        except Exception as e:
            print(f"Erreur lors de la récupération des données : {e}")
            result_dict = {}

        return result_dict

    def readOne(self, id: int) -> Coordinate:
        """
        Read data for a specific ID from the coord table.

        Parameters:
        - id (int): The ID of the entry to retrieve.

        Returns:
        - Coordinate or None: A Coordinate instance if data is found, None otherwise.
        """
        try:
            self.cursor.execute(f"SELECT * FROM coord WHERE id={id};")
            rows = self.cursor.fetchall()

            _, ip, timestamp, latitude, longitude = rows[0]
            result = Coordinate(ip, timestamp, latitude, longitude)

        except Exception as e:
            print(f"Erreur lors de la récupération des données : {e}")
            result = None

        return result

if __name__ == '__main__':
    # Example usage:
    coord_entry = Coordinate(
        latitude=12.345, longitude=45.678, time=datetime.now(), ip="127.0.0.1"
    )
    # DatabaseManager.create_db()
    db_manager = DatabaseManager()
    db_manager.insert_data(coord_entry)

    # Example for readAll
    all_data = db_manager.readAll()
    print(all_data)

    # Example for readOne
    entry_id = 1
    specific_entry = db_manager.readOne(entry_id)
    if specific_entry:
        print(f"Data for ID {entry_id}: {specific_entry.to_json()}")
    else:
        print(f"No data found for ID {entry_id}")
