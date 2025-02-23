from util import get_logger
from .ouilookup import OUILookup
from .network_scanner import NetworkScanner
from pprint import pprint
import subprocess
import re
import time

logger = get_logger(__name__)

class DiscoveryEngine:
    def __init__(self, networks, sleep_interval=15):
        logger.info('Initializing discovery engine.')
        
        self.network_scanner = NetworkScanner(networks)
        self.oui_lookup = OUILookup()
        self.sleep_interval = sleep_interval
        self.data = {ip: {'mac': None, 'vendor': None, 'gateway': None} for ip in self.network_scanner.get_ips()}
    
    
    def set_mac_addresses(self):
        for ip in self.data:
            mac = self.network_scanner.get_mac_address(ip)
            self.data[ip]['mac'] = mac
    
    
    def set_vendors(self):
        for ip in self.data:
            mac = self.data[ip]['mac']
            if mac:
                oui = self.oui_lookup.parse_oui_from_mac(mac)
                vendor = self.oui_lookup.lookup_vendor(oui)
                self.data[ip]['vendor'] = vendor
    
    
    def set_host_gateway(self):
        gateway = self.network_scanner.get_host_gateway()
        if gateway:
            subnet = '.'.join(gateway.split('.')[0:3])
            for ip in self.data:
                if subnet in ip:
                    self.data[ip]['gateway'] = gateway
    
    
    def run(self):
        logger.info('Starting discovery engine.')
        while True:
            self.set_mac_addresses()
            self.set_vendors()
            self.set_host_gateway()
            
            pprint(self.data)
            
            time.sleep(self.sleep_interval)