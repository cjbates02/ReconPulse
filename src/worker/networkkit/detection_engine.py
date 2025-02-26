from scapy.all import ARP, sniff
from util import get_logger

logger = get_logger(__name__)

class DetectionEngine:
    def __init__(self, network):
        self.network = network
        self.known_endpoints = set()
    

    def detect_new_endpoint(self, packet):
        if packet.haslayer(ARP):
            mac = packet.hwsrc
            ip = packet.psrc
            
            if ip not in self.known_endpoints:
                logger.info(f'New device detected: {ip}, {mac}')
                self.known_endpoints.add(ip)
    
    
    def run(self):
        logger.info('Starting discovery engine.')
        sniff(filter='arp', prn=self.detect_new_endpoint, store=0)


if __name__ == '__main__':
    detection_engine = DetectionEngine('10.0.97.0/24')
    detection_engine.run()
    