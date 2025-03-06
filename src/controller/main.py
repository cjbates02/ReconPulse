from discoverykit import DiscoveryEngine, OUILookup
from models import Scanner

""" WILL RUN ON CONTROLLER NODE """

if __name__ == '__main__':
    # sudo $(which python) app.py
    
    # detection_engine = DetectionEngine('10.0.97.0/24')
    # detection_engine.run()
    scanner1 = Scanner(address='10.0.97.212:80', network='10.0.97.0/24')
    scanner2 = Scanner(address='10.0.99.212:80', network='10.0.99.0/24')
    
    discovery_engine = DiscoveryEngine([scanner1, scanner2])
    discovery_engine.run()