from util import get_logger
import subprocess
import re
import time

logger = get_logger(__name__)

class DiscoveryEngine:
    def __init__(self, networks):
        self.networks = networks
        self.new_endpoints = set()
        self.sleep_interval = 15
        
    
    def discover_layer2_endpoints(self):
        try:
            for network in self.networks:
                output = subprocess.check_output(['nmap', '-sn', '-PR', network], text=True)
                ip_addresses = self.parse_ip_addresses(output)
                logger.info(f"Successfully discovered the following ip addresses on network {network}: {ip_addresses}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to execute 'nmap -sn' scan on {self.networks}. Exit code: {e.returncode}")
    
    
    def parse_ip_addresses(self, output):
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        matches = re.findall(ip_pattern, output)
        return matches
    
    
    def run(self):
        logger.info('Starting discovery engine.')
        while True:
            self.discover_layer2_endpoints()
            time.sleep(self.sleep_interval)


if __name__ == '__main__':
    discovery_engine = DiscoveryEngine('10.0.97.0/24')
    discovery_engine.discover_layer2_endpoints()