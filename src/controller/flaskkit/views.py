from flask import jsonify, request
from flask.views import MethodView

class NetworkExporterAPI(MethodView):
    def __init__(self):
        pass

    def get(self):
        ips = self.scanner.get_ips()
        if ips:
            return jsonify(ips), 200
        return 'Could not retrieve IP list.', 201
    
    