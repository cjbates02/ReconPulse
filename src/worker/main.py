from flask import Flask
from views import IPListAPI, MACAddressAPI, GatewayAPI
from dotenv import load_dotenv
from util import get_logger
import os

""" WILL RUN ON WORKER NODES """

logger = get_logger(__name__)

def create_api(network):
    logger.info(f'Creating API routes for network {network}')
    api = Flask(__name__)
    
    api.add_url_rule('/scan/ip_list', view_func=IPListAPI.as_view('ip_list_api', network=network))
    api.add_url_rule('/scan/mac', view_func=MACAddressAPI.as_view('mac_api', network=network))
    api.add_url_rule('/scan/gateway', view_func=GatewayAPI.as_view('gateway_api', network=network))
    
    return api

api = create_api(os.getenv('NETWORK'))

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0')
