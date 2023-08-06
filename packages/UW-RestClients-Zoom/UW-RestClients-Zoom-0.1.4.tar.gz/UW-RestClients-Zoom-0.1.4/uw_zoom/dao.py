"""
Contains UW Zoom DAO implementations.
"""
from restclients_core.dao import DAO
from os.path import abspath, dirname
from time import time
import jwt
import os


class ZOOM_DAO(DAO):
    def service_name(self):
        return 'zoom'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), 'resources'))]

    def _generate_jwt(self):
        headers = {'alg': 'HS256', 'typ': 'JWT'}
        payload = {
            'iss': self.get_service_setting('API_KEY', ''),
            'exp': int(time() + self.get_service_setting('VALID_FOR', 10)),
        }
        secret = self.get_service_setting('API_SECRET', '')
        return jwt.encode(payload, secret, algorithm='HS256', headers=headers)

    def _custom_headers(self, method, url, headers, body):
        token = self._generate_jwt()
        return {'Authorization': 'Bearer {}'.format(token.decode())}
