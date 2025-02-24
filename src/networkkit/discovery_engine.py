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
        
        self.oui_lookup = OUILookup()
        self.sleep_interval = sleep_interval
        self.scanner_to_output = {}
        
        for network in networks:
            scanner = NetworkScanner(network)
            self.scanner_to_output[scanner] = {ip: {} for ip in scanner.get_ips()}
    
    
    def set_mac_addresses(self):
        for scanner in self.scanner_to_output:
            for ip in self.scanner_to_output[scanner]:
                mac = scanner.get_mac_address(ip)
                self.scanner_to_output[scanner][ip]['mac'] = mac

    
    def set_vendors(self):
        for scanner in self.scanner_to_output:
            for ip in self.scanner_to_output[scanner]:
                mac = self.scanner_to_output[scanner][ip]['mac']
                if not mac:
                    logger.error(f'Cannot set vendor for ip {ip} because no mac address was found.')
                    self.scanner_to_output[scanner][ip]['vendor'] = None
                    return
                oui = self.oui_lookup.parse_oui_from_mac(mac)
                vendor = self.oui_lookup.lookup_vendor(oui)
                self.scanner_to_output[scanner][ip]['vendor'] = vendor
    
    
    def set_gateway(self):
        for scanner in self.scanner_to_output:
            gateway = scanner.get_gateway()
            if gateway:
                for ip in self.scanner_to_output[scanner]:
                    self.scanner_to_output[scanner][ip]['gateway'] = gateway
    
    
    def print_output(self):
        for scanner in self.scanner_to_output:
            logger.info(f'Discovered these endpoints on network {scanner.network}:')
            for ip in self.scanner_to_output[scanner]:
                mac = self.scanner_to_output[scanner][ip]['mac']
                vendor = self.scanner_to_output[scanner][ip]['vendor']
                gateway = self.scanner_to_output[scanner][ip]['gateway']
                logger.info(f'IP: {ip}, MAC: {mac}, Vendor: {vendor}, Gateway: {gateway}')
    
    
    def run(self):
        logger.info('Starting discovery engine.')
        while True:
            self.set_mac_addresses()
            self.set_vendors()
            self.set_gateway()
            
            self.print_output()
            
            time.sleep(self.sleep_interval)