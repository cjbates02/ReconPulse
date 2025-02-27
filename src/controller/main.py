from discoverykit import DiscoveryEngine, OUILookup
from models import Scanner

""" WILL RUN ON CONTROLLER NODE """

if __name__ == '__main__':
    # sudo $(which python) app.py
    
    # detection_engine = DetectionEngine('10.0.97.0/24')
    # detection_engine.run()
    scanner = Scanner(address='0.0.0.0:80', network='10.0.97.0/24')
    discovery_engine = DiscoveryEngine([scanner])
    discovery_engine.run()