from requests import get
from .types import ( ClientInfo, StatementItem, MonoCard)
    
BASE_URL = 'https://api.monobank.ua'

class OpenMono:
    __HEADERS = {
        'Request Content-Types': 'application/json',
        'Response Content-Types': 'application/json', 
        'Schemes': 'https', 
        'Version': '201906' }

    def __init__(self, token, version = None):
        self._TOKEN = token
        if version:
            OpenMono.__HEADERS['Version'] = str(version)

    @property
    def __headers(self):
        return {**OpenMono.__HEADERS, **{'X-Token': self._TOKEN}}

    def _get(self, url):
        return get(BASE_URL+url, headers=self.__headers).json() 

    def client_info(self):
        response = self._get('/personal/client-info')
        response['accounts'] = [ MonoCard(i, self) for i in response['accounts'] ]

        return ClientInfo(response)

