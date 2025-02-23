from util import get_logger
import subprocess
import re

logger = get_logger(__name__)

class NetworkScanner:
    def __init__(self, networks):
        self.networks = networks
    
    
    def get_ips(self):
        try:
            for network in self.networks:
                output = subprocess.check_output(['nmap', '-sn', '-PR', network], text=True)
                ips = self._parse_ip_addresses(output)
                logger.info(f"Successfully discovered the following ip addresses on network {network}: {ips}")
            return ips
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to execute 'nmap -sn' scan on {self.networks}. Exit code: {e.returncode}")
            return []
    
    
    def _parse_ip_addresses(self, output):
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, output)
        return ips
    
    
    def get_mac_address(self, ip):
        try:
            output = subprocess.check_output(['arp', '-a', ip], text=True)
            mac = self._parse_mac_address(output)
            logger.info(f"Successfully discovered mac address {mac} for ip address {ip}.")
            return mac
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to execute 'arp -a' scan on {self.networks}. Exit code: {e.returncode}.")
    
    
    def _parse_mac_address(self, output):
        mac_pattern = r'(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}'
        match = re.search(mac_pattern, output)
        mac = match.group() if match else None
        return mac
            

    def get_host_gateway(self):
        try:
            output = subprocess.check_output(['ip', 'route'], text=True)
            gateway = re.search(r'default via \b(?:\d{1,3}\.){3}\d{1,3}\b', output).group().split()[-1].strip()
            logger.info(f"Successfully discovered host gateway: {gateway}.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to execute 'ip route' command. Exit code: {e.returncode}.")
            gateway = None
        return gateway
    
    