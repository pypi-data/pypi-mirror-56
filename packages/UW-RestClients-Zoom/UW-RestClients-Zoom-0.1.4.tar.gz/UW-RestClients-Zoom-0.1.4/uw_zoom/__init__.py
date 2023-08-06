from uw_zoom.dao import ZOOM_DAO
from restclients_core.exceptions import DataFailureException
from urllib.parse import urlencode
import json


class ZOOM(object):
    def __init__(self, config={}):
        self.DAO = ZOOM_DAO()
        self.PAGE_SIZE = 300  # max page size = 300

    def _get_paged_resource(self, url, key):
        params = {'page_size': self.PAGE_SIZE}
        response = self._get_resource(url, params)
        data = response[key]

        if response.get('page_count', 1) > 1:
            for page_number in range(2, response['page_count'] + 1):
                params['page_number'] = page_number
                response = self._get_resource(url, params)
                data.extend(response[key])
        return data

    def _get_resource(self, url, params={}):
        if len(params):
            url += '?' + urlencode(params)
        response = self.DAO.getURL(url, self._headers())

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _patch_resource(self, url, body):
        response = self.DAO.patchURL(url, body, self._headers())

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _delete_resource(self, url, params={}):
        if len(params):
            url += '?' + urlencode(params)
        response = self.DAO.deleteURL(url, self._headers())

        if response.status != 204 and response.status != 200:
            raise DataFailureException(url, response.status, response.data)
        return response

    def _headers(self):
        headers = {'Accept': 'application/json'}
        return headers
