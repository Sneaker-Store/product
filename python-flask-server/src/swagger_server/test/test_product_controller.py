# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.product import Product  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProductController(BaseTestCase):
    """ProductController integration test stubs"""

    def test_delete_product(self):
        """Test case for delete_product

        delete product by query
        """
        response = self.client.open(
            '/v1/products',
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_product_by_id(self):
        """Test case for delete_product_by_id

        delete product by id
        """
        response = self.client.open(
            '/v1/products/{prodID}'.format(prodID=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_product_by_id(self):
        """Test case for get_product_by_id

        get product by id
        """
        response = self.client.open(
            '/v1/products/{prodID}'.format(prodID=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_product_by_query(self):
        """Test case for get_product_by_query

        get product by query
        """
        response = self.client.open(
            '/v1/products',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_product(self):
        """Test case for post_product

        post product
        """
        response = self.client.open(
            '/v1/products',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
