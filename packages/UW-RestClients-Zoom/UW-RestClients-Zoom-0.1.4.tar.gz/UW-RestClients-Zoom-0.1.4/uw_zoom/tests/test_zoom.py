from unittest import TestCase
from uw_zoom import ZOOM
from uw_zoom.dao import ZOOM_DAO
from restclients_core.models import MockHTTP
from restclients_core.exceptions import DataFailureException
import mock


class ZoomAPITest(TestCase):
    def setUp(self):
        self.success_response = MockHTTP()
        self.success_response.status = 200
        self.success_response.data = b'{}'

        self.error_response = MockHTTP()
        self.error_response.status = 404
        self.error_response.data = b''

    @mock.patch.object(ZOOM, '_get_resource')
    def test_get_paged_resource(self, mock_get):
        zoom = ZOOM()

        # One page returned
        mock_get.return_value = {'page_count': 1, 'test': []}
        resp = zoom._get_paged_resource('/api/test', 'test')
        mock_get.assert_called_with(
            '/api/test', {'page_size': zoom.PAGE_SIZE})

        # More than one page returned
        mock_get.return_value = {'page_count': 2, 'test': []}
        resp = zoom._get_paged_resource('/api/test', 'test')
        mock_get.assert_called_with(
            '/api/test', {'page_size': 300, 'page_number': 2})

    @mock.patch.object(ZOOM_DAO, 'getURL')
    def test_get_resource(self, mock_get):
        zoom = ZOOM()

        mock_get.return_value = self.success_response
        resp = zoom._get_resource('/api/test')
        mock_get.assert_called_with(
            '/api/test', {'Accept': 'application/json'})

        resp = zoom._get_resource('/api/test', {'test': True})
        mock_get.assert_called_with(
            '/api/test?test=True', {'Accept': 'application/json'})

        mock_get.return_value = self.error_response
        self.assertRaises(
            DataFailureException, zoom._get_resource, '/api/test')

    @mock.patch.object(ZOOM_DAO, 'patchURL')
    def test_patch_resource(self, mock_patch):
        zoom = ZOOM()

        mock_patch.return_value = self.success_response
        resp = zoom._patch_resource('/api/test', body={'Test': True})
        mock_patch.assert_called_with(
            '/api/test', {'Test': True}, {'Accept': 'application/json'})

        mock_patch.return_value = self.error_response
        self.assertRaises(
            DataFailureException, zoom._patch_resource, '/api/test', body={})

    @mock.patch.object(ZOOM_DAO, 'deleteURL')
    def test_delete_resource(self, mock_delete):
        zoom = ZOOM()

        mock_delete.return_value = self.success_response
        resp = zoom._delete_resource('/api/test')
        mock_delete.assert_called_with(
            '/api/test', {'Accept': 'application/json'})

        resp = zoom._delete_resource('/api/test', {'test': True})
        mock_delete.assert_called_with(
            '/api/test?test=True', {'Accept': 'application/json'})

        mock_delete.return_value = self.error_response
        self.assertRaises(
            DataFailureException, zoom._delete_resource, '/api/test')

    def test_request_headers(self):
        zoom = ZOOM()
        self.assertEquals(zoom._headers(), {'Accept': 'application/json'})
