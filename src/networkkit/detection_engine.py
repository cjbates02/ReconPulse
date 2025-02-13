from scapy.all import ARP, sniff

class DetectionEngine:
    def __init__(self, network):
        self.network = network
        self.known_endpoints = set()
    

    def detect_new_endpoint(self, packet):
        if packet.haslayer(ARP): # it is an arp response not a request
            mac = packet.hwsrc
            ip = packet.psrc
            
            if ip not in self.known_endpoints:
                print(f'New device detected: {ip}, {mac}')
                self.known_endpoints.add(ip)
    
    
    def run(self):
        print('Starting discovery engine.')
        sniff(filter="arp", prn=self.detect_new_endpoint, store=0)


if __name__ == '__main__':
    # sudo $(which python) discovery.py
    detection_engine = DetectionEngine('10.0.97.0/24')
    detection_engine.run()
    