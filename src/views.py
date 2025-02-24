from flask import jsonify, request
from flask.views import MethodView
from networkkit import NetworkScanner

class NetworkAPI(MethodView):
    def __init__(self, network):
        self.scanner = NetworkScanner(network)
    
    
    def get(self):
        action = ip = request.args.get('action')
        if not action:
            return jsonify({'error': 'Missing action.'}), 400
        
        if action == 'ips':
            return jsonify(self.scanner.get_ips())
        
        if action == 'mac':
            ip = request.args.get('ip')
            if not ip:
                return jsonify({'error': 'Missing IP address.'}), 400
            return jsonify(self.scanner.get_mac_address(ip))
        
        if action == 'gateway':
            return jsonify(self.scanner.get_gateway())
   
        return jsonify({'error': 'Invalid action.'}), 400