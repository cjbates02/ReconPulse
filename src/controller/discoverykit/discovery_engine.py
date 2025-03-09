from util import get_logger
from .ouilookup import OUILookup
from databasekit import NetworkDatabase
from pprint import pprint
import re
import time
import requests

logger = get_logger(__name__)

class DiscoveryEngine:
    def __init__(self, scanners, sleep_interval=15):
        logger.info('Initializing discovery engine.')
        
        self.oui_lookup = OUILookup()
        self.db = NetworkDatabase()
        
        self.sleep_interval = sleep_interval
        self.network_to_output = {}
        self.scanners = scanners
    
    
    def send_scanner_request(self, scanner, value, request_arg=None):
        try:
            if request_arg:
                response = requests.get(f"http://{scanner.address}/scan/{value}?{request_arg['name']}={request_arg['value']}")
            else:
                response = requests.get(f'http://{scanner.address}/scan/{value}')
        except requests.exceptions.ConnectionError as e:
            logger.error(f'Could not connect to worker node {scanner.address}.')
            return None
            
        if not response:
            logger.error(f'Failed to send {value} request to scanner {scanner.address}.')
            return None
        
        if response.status_code == 200:
            return response.json()
        if response.status_code == 201:
            logger.error(f'{response.text}')
        if response.status_code == 400:
            logger.error(f'{response.text}')
        return None
    
    
    def set_ips(self):
        for scanner in self.scanners:
            ip_list = self.send_scanner_request(scanner, 'ip_list')
            if not ip_list:
                ip_list = []
            self.network_to_output[scanner.network] = {ip: {} for ip in ip_list}
    
    
    def set_mac_addresses(self):
        for scanner in self.scanners:
            for ip in self.network_to_output[scanner.network]:
                mac = self.send_scanner_request(scanner, 'mac', request_arg={'name': 'ip', 'value': ip})
                self.network_to_output[scanner.network][ip]['mac'] = mac

    
    def set_vendors(self):
        for scanner in self.scanners:
            for ip in self.network_to_output[scanner.network]:
                mac = self.network_to_output[scanner.network][ip]['mac']
                if not mac:
                    logger.error(f'Cannot set vendor for ip {ip} because no mac address was found.')
                    self.network_to_output[scanner.network][ip]['vendor'] = None
                    continue
                oui = self.oui_lookup.parse_oui_from_mac(mac)
                vendor = self.oui_lookup.lookup_vendor(oui)
                self.network_to_output[scanner.network][ip]['vendor'] = vendor
    
    
    def set_gateway(self):
        for scanner in self.scanners:
            gateway = self.send_scanner_request(scanner, 'gateway')
            if gateway:
                for ip in self.network_to_output[scanner.network]:
                    self.network_to_output[scanner.network][ip]['gateway'] = gateway
                
    
    def create_records(self):
        for scanner in self.scanners:
            logger.info(f'Discovered these endpoints on network {scanner.network}:')
            for ip in self.network_to_output[scanner.network]:
                mac = self.network_to_output[scanner.network][ip].get('mac')
                vendor = self.network_to_output[scanner.network][ip].get('vendor')
                gateway = self.network_to_output[scanner.network][ip].get('gateway')
                logger.info(f'IP: {ip}, MAC: {mac}, Vendor: {vendor}, Gateway: {gateway}')
                self.db.insert_record(ip, mac, vendor, gateway)
                
    
    
    def run(self):
        logger.info('Starting discovery engine.')
        while True:
            self.set_ips()
            self.set_mac_addresses()
            self.set_vendors()
            self.set_gateway()
            
            self.create_records()
            logger.info('\n\nRecords from 2025-03-09 14:35:21')
            logger.info(self.db.retrieve_record('2025-03-09 23:44:49'))
            
            self.network_to_output = {}
            time.sleep(self.sleep_interval)