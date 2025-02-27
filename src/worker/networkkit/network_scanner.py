from util import get_logger, execute_subprocess_command
import subprocess
import re

logger = get_logger(__name__)

class NetworkScanner:
    def __init__(self, network):
        self.network = network

    
    def get_ips(self):
        output = execute_subprocess_command(f'nmap -sn -PR {self.network}')
        ips = self._parse_ip_addresses(output)
        if not ips:
            logger.error(f'Failed to discover any ips on network {self.network}')
        return ips
        
    
    def _parse_ip_addresses(self, output):
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, output)
        return ips
    
    
    def get_mac_address(self, ip):
        output = execute_subprocess_command(f'arp -a {ip}')
        mac = self._parse_mac_address(output)
        if not mac:
            logger.error(f'Failed to find mac address for ip {ip}.')
        return mac

    
    def _parse_mac_address(self, output):
        match = re.search(r'(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}', output)
        mac = match.group() if match else None
        return mac
            

    def get_gateway(self):
        output = execute_subprocess_command('ip route')
        gateway = self._parse_gateway(output)
        if not gateway:
            logger.error(f'Failed to find host gateway.')
        return gateway
    
    
    def _parse_gateway(self, output):
        match = re.search(r'default via \b(?:\d{1,3}\.){3}\d{1,3}\b', output)
        gateway = match.group().split()[-1].strip() if match else None
        return gateway
        
        
    
    