import json

import requests

from data.config import BASE_URL


class API:
    def storage_products_quantity(self):
        products_quantity = requests.get(f'{BASE_URL}/v1/storage/products_quantity/')
        products_quantity = json.loads(products_quantity.text)
        return products_quantity

    def storage_products_info(self):
        products_info = requests.get(f'{BASE_URL}/v1/storage/products_info/')
        products_info = json.loads(products_info.text)
        return products_info

    def storage_product_quantity(self, pk, json_patch):
        requests.patch(f'{BASE_URL}/v1/storage/product_quantity/{pk}/', json=json_patch)


    def storage_product_info(self, pk):
        product_info = requests.get(f'{BASE_URL}/v1/storage/product_info/{pk}/')
        product_info = json.loads(product_info.text)
        return product_info
