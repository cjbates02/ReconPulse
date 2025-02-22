from util import get_logger
from scapy.all import ARP, Ether, srp
from pprint import pprint
import subprocess
import re
import time
import requests

logger = get_logger(__name__)

OUI_URL = 'https://standards-oui.ieee.org/'

class DiscoveryEngine:
    def __init__(self, networks):
        self.networks = networks
        self.sleep_interval = 15
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.oui_cache = self.fetch_oui_data()
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
    
    
    def set_mac_addresses(self):
        try:
            for ip in self.data:
                output = subprocess.check_output(['arp', '-a', ip], text=True)
                mac = self.parse_mac_address(output)
                self.data[ip]['mac'] = mac
                logger.info(f"Successfully discovered mac address {mac} for ip address {ip}.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to execute 'arp -a' scan on {self.networks}. Exit code: {e.returncode}.")
    
    
    def set_vendors(self):
        for ip in self.data:
            mac = self.data[ip]['mac']
            if mac:
                oui = self.parse_oui_from_mac(mac)
                vendor = self.lookup_vendor(oui)
                self.data[ip]['vendor'] = vendor
                
    
    def parse_oui_from_mac(self, mac):
        oui = '-'.join(mac.split(':')[0:3]).upper()
        return oui
    
    
    def lookup_vendor(self, oui):
        if oui and oui in self.oui_cache:
            vendor = re.search(f'{oui}.*', self.oui_cache).group().split('\t')[2].strip()
            logger.info(f'Vendor found in oui cache: {vendor}.')
            return vendor
        logger.error(f'OUI not found in oui cache: {oui}.')
        return None
    
    
    def fetch_oui_data(self):
        response = requests.get(OUI_URL, headers=self.headers)
        if response.status_code == 200:
            logger.info('Successfully fetched oui data.')
            return response.text
        logger.error('Failed to fetch oui data. Response code: ', response.status_code)
        return None
    
    
    def parse_ip_addresses(self, output):
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, output)
        return ips
    
    
    def parse_mac_address(self, output):
        mac_pattern = r'(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}'
        match = re.search(mac_pattern, output)
        mac = match.group() if match else None
        return mac
    
    
    def run(self):
        logger.info('Starting discovery engine.')
        while True:
            self.discover_layer2_endpoints()
            self.set_mac_addresses()
            self.set_vendors()
            pprint(self.data)
            time.sleep(self.sleep_interval)