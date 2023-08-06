from unittest import TestCase
from uw_zoom.utilities import fdao_zoom_override
from uw_zoom.models import ZoomUser
from uw_zoom.users import Users
import datetime
import pytz
import mock


@fdao_zoom_override
class UsersAPITest(TestCase):
    def test_get_users(self):
        zoom = Users()
        users = zoom.get_users()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].first_name, "Melina")
        self.assertEqual(users[1].first_name, "Bill")
        created_dt = datetime.datetime(year=2018,
                                       month=11,
                                       day=15,
                                       hour=1,
                                       minute=10,
                                       second=8,
                                       tzinfo=pytz.UTC)
        self.assertEqual(users[0].created_at, created_dt)

    def test_get_user_settings(self):
        zoom = Users()
        settings = zoom.get_user_settings('z8yAAAAA8bbbQ')
        self.assertEqual(settings['feature']['large_meeting'], False)
        self.assertEqual(settings['feature']['meeting_capacity'], 100)

    @mock.patch.object(Users, '_patch_resource')
    def test_update_user_settings(self, mock_patch):
        zoom = Users()
        settings = zoom.get_user_settings('z8yAAAAA8bbbQ')
        settings['feature']['large_meeting'] = True
        settings['feature']['meeting_capacity'] = 500
        resp = zoom.update_user_settings('z8yAAAAA8bbbQ', settings)
        mock_patch.assert_called_with(
            '/v2/users/z8yAAAAA8bbbQ/settings', settings)

    @mock.patch.object(Users, '_patch_resource')
    def test_update_type(self, mock_patch):
        zoom = Users()
        resp = zoom.update_user_type('z8yAAAAA8bbbQ', ZoomUser.TYPE_BASIC)
        mock_patch.assert_called_with(
            '/v2/users/z8yAAAAA8bbbQ', {'type': ZoomUser.TYPE_BASIC})

    @mock.patch.object(Users, '_delete_resource')
    def test_delete_user(self, mock_delete):
        zoom = Users()
        resp = zoom.delete_user('z8yAAAAA8bbbQ', is_delete=True)
        mock_delete.assert_called_with(
            '/v2/users/z8yAAAAA8bbbQ', {'action': 'delete'})

        resp = zoom.delete_user('z8yAAAAA8bbbQ')
        mock_delete.assert_called_with('/v2/users/z8yAAAAA8bbbQ', {})
