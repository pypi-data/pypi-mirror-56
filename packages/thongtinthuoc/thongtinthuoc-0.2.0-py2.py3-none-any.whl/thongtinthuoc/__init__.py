import requests
from munch import *

class Thongtinthuoc:
    root = 'https://thongtinthuoc.com/api/v1'

    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, objtype, query):
        url = '/'.join([self.root, 'search'])
        api_key = self.api_key
        # api_key = ']sFwDb8;$Zp0TpK3:k@JIZe0C=7BO7'
        # query = 'paracetamol'
        # objtype = 'bietduoc'
        response = requests.get(
            url,
            headers={ 'X-API-KEY': api_key },
            params={ 's': query, 'e': objtype }
        )

        result = munchify(response.json())
        return result

    def search_brand(self, query):
        return search(query, 'bietduoc', query)

    def search_unii(self, query):
        return search(query, 'unii', query)

    def search_ingredient(self, query):
        return search(query, 'duoclieu', query)

    def search_pharmacy(self, query):
        return search(query, 'doanhnghiep', query)
