from util import get_logger
import requests
import re

logger = get_logger(__name__)
OUI_URL = 'https://standards-oui.ieee.org/'

class OUILookup:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.oui_cache = self._fetch_oui_data()
    
    
    def _fetch_oui_data(self):
        response = requests.get(OUI_URL, headers=self.headers)
        if response.status_code == 200:
            logger.info('Successfully fetched oui data.')
            return response.text
        logger.error(f'Failed to fetch oui data. Response code: {response.status_code}')
        return None
    

    def lookup_vendor(self, oui):
        if oui and oui in self.oui_cache:
            vendor = re.search(f'{oui}.*', self.oui_cache).group().split('\t')[2].strip()
            return vendor
        logger.error(f'OUI not found in oui cache: {oui}.')
        return None
    
    
    def parse_oui_from_mac(self, mac):
        oui = '-'.join(mac.split(':')[0:3]).upper()
        return oui
    
    
    
    
    