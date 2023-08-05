import requests
from munch import *

class Thongtinthuoc:
    root = 'https://thongtinthuoc.com/api/v1'

    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, objtype, query, page=1, size=12):
        url = '/'.join([self.root, 'search'])
        api_key = self.api_key

        # url = 'https://thongtinthuoc.com/api/v1/search'
        # api_key = ']sFwDb8;$Zp0TpK3:k@JIZe0C=7BO7'
        # query = 'paracetamol'
        # objtype = 'bietduoc'
        # page = 2
        # size = 20
        response = requests.get(
            url,
            headers={ 'X-API-KEY': api_key },
            params={
                's': query,
                'e': objtype,
                'page': page,
                'size': size,
            }
        )

        result = munchify(response.json())
        return result

    def search_brand(self, query, **kwargs):
        return search(query, 'bietduoc', **kwargs)

    def search_unii(self, query, **kwargs):
        return search(query, 'unii', **kwargs)

    def search_ingredient(self, query, **kwargs):
        return search(query, 'duoclieu', **kwargs)

    def search_pharmacy(self, query, **kwargs):
        return search(query, 'doanhnghiep', **kwargs)
