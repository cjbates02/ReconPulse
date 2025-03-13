import sqlite3
import threading

class NetworkDatabase:
    def __init__(self):
        self.db_file_path = 'network.db'
        self.network_exporter_table = 'network_exporter'
        self._lock = threading.Lock()
        self.initalize_database()
    
    
    def _connect_db(self):
        return sqlite3.connect(self.db_file_path)
    
    
    def execute_query(self, query):
        with self._connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
    
    
    def initalize_database(self):
        self.execute_query(f'''
            CREATE TABLE IF NOT EXISTS {self.network_exporter_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                mac TEXT,
                vendor TEXT,
                gateway TEXT,
                timestamp TEXT,
                network TEXT
            )
        ''')
        
    
    def insert_record(self, ip, mac, vendor, gateway, timestamp, network):
        with self._lock:
            with self._connect_db() as connection:
                cursor = connection.cursor()
                cursor.execute(f'INSERT INTO {self.network_exporter_table} (ip, mac, vendor, gateway, timestamp, network) VALUES (? ,? ,? ,?, ?, ?)', (ip, mac, vendor, gateway, timestamp, network,))
                connection.commit()
        
    
    def retrieve_record(self, timestamp):
        with self._connect_db() as connection:
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM {self.network_exporter_table} WHERE timestamp = ?', (timestamp,))
            record = cursor.fetchall()
            return record
        
    
    
    
    
    