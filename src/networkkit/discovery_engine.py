from util import get_logger
from scapy.all import ARP, Ether, srp
import subprocess
import re
import time

logger = get_logger(__name__)

class DiscoveryEngine:
    def __init__(self, networks):
        self.networks = networks
        self.sleep_interval = 15
        self.data = {}
        
    
    def discover_layer2_endpoints(self):
        try:
            for network in self.networks:
                output = subprocess.check_output(['nmap', '-sn', '-PR', network], text=True)
                ips = self.parse_ip_addresses(output)
                self.data = {ip: {'mac': None, 'hostname': None, 'vendor': None} for ip in ips}
                logger.info(f"Successfully discovered the following ip addresses on network {network}: {ips}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to execute 'nmap -sn' scan on {self.networks}. Exit code: {e.returncode}")
    
    
    def parse_ip_addresses(self, output):
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, output)
        return ips
    
    
    def parse_mac_address(self, output):
        mac_pattern = r'(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}'
        match = re.search(mac_pattern, output)
        mac = match.group() if match else None
        return mac
    
    # curl https://api.macvendors.com/5c:26:0a:b3:8c:7a
    def get_mac_addresses(self):
        try:
            for ip in self.data:
                output = subprocess.check_output(['arp', '-a', ip], text=True)
                mac = self.parse_mac_address(output)
                self.data[ip]['mac'] = mac
                logger.info(f"Successfully discovered mac address {mac} for ip address {ip}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to execute 'arp -a' scan on {self.networks}. Exit code: {e.returncode})")
                
        
    def scan_ip_addresses(self):
        pass
    
    
    def run(self):
        logger.info('Starting discovery engine.')
        while True:
            self.discover_layer2_endpoints()
            self.get_mac_addresses()
            print(self.data)
            time.sleep(self.sleep_interval)


if __name__ == '__main__':
    discovery_engine = DiscoveryEngine('10.0.97.0/24')
    discovery_engine.discover_layer2_endpoints()