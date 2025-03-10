from flask import jsonify, request
from flask.views import MethodView
from databasekit import NetworkDatabase

class NetworkExporterAPI(MethodView):
    def __init__(self, discovery_engine):
        self.discovery_engine = discovery_engine
        self.db_conn = NetworkDatabase()

    def get(self):
        if self.discovery_engine.get_latest_poll_time():
            records = self.db_conn.retrieve_record(self.discovery_engine.get_latest_poll_time())
            return jsonify(records), 200
        return f'No records found yet', 201
    
    
    
    