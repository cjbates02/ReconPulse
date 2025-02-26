from flask import Flask
from views import IPListAPI, MACAddressAPI, GatewayAPI

""" WILL RUN ON WORKER NODES """

api = Flask(__name__)

def register_url_rules(network):
    api.add_url_rule('/scan/ip_list', view_func=IPListAPI.as_view('ip_list_api', network=network))
    api.add_url_rule('/scan/mac', view_func=MACAddressAPI.as_view('mac_api', network=network))
    api.add_url_rule('/scan/gateway', view_func=GatewayAPI.as_view('gateway_api', network=network))

if __name__ == '__main__':
    register_url_rules('10.0.97.0/24')
    api.run(debug=True, host='0.0.0.0')
