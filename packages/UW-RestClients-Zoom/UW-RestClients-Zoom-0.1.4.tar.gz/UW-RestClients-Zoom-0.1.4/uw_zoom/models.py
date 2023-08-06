from restclients_core import models
from dateutil.parser import parse


class ZoomAccount(models.Model):
    id = models.CharField(max_length=64)
    account_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=64)
    owner_email = models.CharField(max_length=512)
    account_type = models.CharField(max_length=64)
    seats = models.IntegerField()
    subscription_start_time = models.DateTimeField()
    subscription_end_time = models.DateTimeField()
    created_at = models.DateTimeField()

    @staticmethod
    def from_json(data):
        account = ZoomAccount()
        account.id = data['id']
        account.account_name = data['account_name']
        account.account_number = data['account_number']
        account.owner_email = data['owner_email']
        account.account_type = data['account_type']
        account.seats = data['seats']
        account.subscription_start_time = parse(
            data['subscription_start_time'])
        account.subscription_end_time = parse(data['subscription_end_time'])
        account.created_at = parse(data['created_at'])
        return account


class ZoomUser(models.Model):
    TYPE_BASIC = 1
    TYPE_PRO = 2
    TYPE_CORP = 3
    TYPE_CHOICES = (
        (TYPE_BASIC, 'Basic'), (TYPE_PRO, 'Pro'), (TYPE_CORP, 'Corp')
    )

    id = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    email = models.CharField(max_length=500)
    type = models.IntegerField(choices=TYPE_CHOICES)
    status = models.CharField(max_length=64)
    pmi = models.IntegerField()
    timezone = models.CharField(max_length=255, null=True)
    dept = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField()
    last_login_time = models.DateTimeField(null=True)
    verified = models.IntegerField()

    @staticmethod
    def from_json(data):
        user = ZoomUser()
        user.id = data['id']
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data['email']
        user.type = data['type']
        user.status = data['status']
        user.pmi = data['pmi']
        user.timezone = data.get('timezone')
        user.dept = data.get('dept')
        user.verified = data['verified']
        user.created_at = parse(data['created_at'])
        user.settings = data.get('settings')
        if 'last_login_time' in data:
            user.last_login_time = parse(data['last_login_time'])
        return user
