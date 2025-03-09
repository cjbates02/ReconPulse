import sqlite3

class NetworkDatabase:
    def __init__(self):
        self.db_file_path = 'network.db'
        self.network_exporter_table = 'network_exporter'
        self.connection = sqlite3.connect(self.db_file_path)
        
        self.initalize_database()
    
    
    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
    
    
    def initalize_database(self):
        self.execute_query(f'''
            CREATE TABLE IF NOT EXISTS {self.network_exporter_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                ip TEXT,
                mac TEXT,
                vendor TEXT,
                gateway TEXT
            )
        ''')
        
    
    def insert_record(self, ip, mac, vendor, gateway):
        cursor = self.connection.cursor()
        cursor.execute(f'INSERT INTO {self.network_exporter_table} (ip, mac, vendor, gateway) VALUES (? ,? ,? ,?)', (ip, mac, vendor, gateway,))
        self.connection.commit()
        cursor.close()
        
    
    def retrieve_record(self, timestamp):
        cursor = self.connection.cursor()
        # cursor.execute(f'SELECT * FROM {self.network_exporter_table}')
        cursor.execute(f'SELECT * FROM {self.network_exporter_table} WHERE timestamp = ?', (timestamp,))
        record = cursor.fetchall()
        return record
        
    
    
    
    
    