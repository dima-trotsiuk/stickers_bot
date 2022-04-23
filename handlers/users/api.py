import json

import requests

from data.config import BASE_URL, AUTH_TOKEN


class API:
    headers = {
        "Authorization": f"Token {AUTH_TOKEN}",
    }

    def storage_products_quantity(self):
        products_quantity = requests.get(f'{BASE_URL}/v1/storage/products_quantity/', headers=self.headers)
        products_quantity = json.loads(products_quantity.text)
        return products_quantity

    def storage_products_info(self):
        products_info = requests.get(f'{BASE_URL}/v1/storage/products_info/', headers=self.headers)
        products_info = json.loads(products_info.text)

        return products_info

    def storage_product_quantity_update(self, pk, json_patch):
        requests.patch(f'{BASE_URL}/v1/storage/product_quantity_update/{pk}/', json=json_patch, headers=self.headers)

    def storage_product_quantity(self, pk):
        product_info = requests.get(f'{BASE_URL}/v1/storage/product_quantity/{pk}/', headers=self.headers)
        product_info = json.loads(product_info.text)
        return product_info

    def storage_product_info(self, pk):
        product_info = requests.get(f'{BASE_URL}/v1/storage/product_info/{pk}/', headers=self.headers)
        product_info = json.loads(product_info.text)
        return product_info

    def bag_products_get_post(self, json_post=False):
        if json_post:
            return requests.post(f'{BASE_URL}/v1/bag/bag_products/', data=json_post, headers=self.headers)
        else:
            products_in_bag = requests.get(f'{BASE_URL}/v1/bag/bag_products/', headers=self.headers)
            products_in_bag = json.loads(products_in_bag.text)
            return products_in_bag

    def bag_product_get_update(self, pk, json_patch=False):
        if json_patch:
            requests.patch(f'{BASE_URL}/v1/bag/bag_product/{pk}/', json=json_patch, headers=self.headers)
        else:
            product_in_bag = requests.get(f'{BASE_URL}/v1/bag/bag_product/{pk}/', headers=self.headers)
            product_in_bag = json.loads(product_in_bag.text)
            return product_in_bag

    def bag_plus_product_get_update(self, pk, json_patch=False):
        bag_plus_product = requests.get(f'{BASE_URL}/v1/bag/detail/{pk}/', headers=self.headers)
        bag_plus_product = json.loads(bag_plus_product.text)
        return bag_plus_product

    def bag_detail_get_update(self, pk, json_patch=False):
        if json_patch:
            requests.patch(f'{BASE_URL}/v1/bag/detail/{pk}/', json=json_patch, headers=self.headers)
        else:
            bag_detail = requests.get(f'{BASE_URL}/v1/bag/detail/{pk}/', headers=self.headers)
            bag_detail = json.loads(bag_detail.text)
            return bag_detail

    def bag_create(self, pk):
        bag_detail = requests.get(f'{BASE_URL}/v1/bag/create/{pk}/', headers=self.headers)
        return bag_detail
