from unittest import TestCase
from uw_zoom.utilities import fdao_zoom_override
from uw_zoom.models import ZoomAccount, ZoomUser
from uw_zoom.accounts import Accounts
import datetime
import pytz
import mock


@fdao_zoom_override
class AccountsAPITest(TestCase):
    def test_get_sub_accounts(self):
        zoom = Accounts()
        accounts = zoom.get_sub_accounts()
        self.assertEqual(len(accounts), 3)
        self.assertEqual(accounts[0].account_number, 1)
        self.assertEqual(accounts[0].account_name, 'Zoom 1')
        self.assertEqual(accounts[0].seats, 1000)

    @mock.patch.object(Accounts, '_get_paged_resource')
    def test_get_account_users(self, mock_get):
        zoom = Accounts()
        resp = zoom.get_account_users(account_id='123')
        mock_get.assert_called_with('/v2/accounts/123/users', key='users')

    @mock.patch.object(Accounts, '_patch_resource')
    def test_update_account_user_type(self, mock_patch):
        zoom = Accounts()
        resp = zoom.update_account_user_type(
            '123', 'z8yAAAAA8bbbQ', ZoomUser.TYPE_BASIC)
        mock_patch.assert_called_with('/v2/accounts/123/users/z8yAAAAA8bbbQ',
                                      {'type': ZoomUser.TYPE_BASIC})

    @mock.patch.object(Accounts, '_get_resource')
    def test_get_account_user_settings(self, mock_get):
        zoom = Accounts()
        resp = zoom.get_account_user_settings('123', 'z8yAAAAA8bbbQ')
        mock_get.assert_called_with(
            '/v2/accounts/123/users/z8yAAAAA8bbbQ/settings')

    @mock.patch.object(Accounts, '_patch_resource')
    def test_patch_account_user_settings(self, mock_patch):
        zoom = Accounts()
        resp = zoom.update_account_user_settings(
            '123', 'z8yAAAAA8bbbQ', {'abc': True})
        mock_patch.assert_called_with(
            '/v2/accounts/123/users/z8yAAAAA8bbbQ/settings',
            {'abc': True})
