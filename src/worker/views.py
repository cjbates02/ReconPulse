from flask import jsonify, request
from flask.views import MethodView
from networkkit import NetworkScanner

class IPListAPI(MethodView):
    def __init__(self, network):
        self.scanner = NetworkScanner(network)

    def get(self):
        ips = self.scanner.get_ips()
        if ips:
            return jsonify(ips), 200
        return 'Could not retrieve IP list.', 201


class MACAddressAPI(MethodView):
    def __init__(self, network):
        self.scanner = NetworkScanner(network)

    def get(self):
        ip = request.args.get('ip')
        if not ip:
            return 'Missing IP address.', 400
        mac = self.scanner.get_mac_address(ip)
        if mac:
            return jsonify(mac), 200
        return f'MAC Address not found for ip {ip}', 201


class GatewayAPI(MethodView):
    def __init__(self, network):
        self.scanner = NetworkScanner(network)

    def get(self):
        gateway = self.scanner.get_gateway()
        if gateway:
            return jsonify(gateway), 200
        return 'Gateway not found.', 201