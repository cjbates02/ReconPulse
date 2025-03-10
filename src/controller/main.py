from discoverykit import DiscoveryEngine
from models import Scanner
from flask import Flask
from views import NetworkExporterAPI
import time

""" WILL RUN ON CONTROLLER NODE """

def create_api(discovery_engine):
    api = Flask(__name__)
    api.add_url_rule('/network_exporter', view_func=NetworkExporterAPI.as_view('network_exporter', discovery_engine=discovery_engine))
    return api

if __name__ == '__main__':
    # sudo $(which python) app.py
    
    # detection_engine = DetectionEngine('10.0.97.0/24')
    # detection_engine.run()
    scanner1 = Scanner(address='10.0.97.212:80', network='10.0.97.0/24')
    scanner2 = Scanner(address='10.0.99.212:80', network='10.0.99.0/24')
    
    discovery_engine = DiscoveryEngine([scanner1, scanner2])
    api = create_api(discovery_engine)
    api.run(debug=True, host='0.0.0.0')