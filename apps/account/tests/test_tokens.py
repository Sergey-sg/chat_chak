from django.test import TestCase
from django.utils import six

from apps.account.models import User
from apps.account.tokens import TokenGenerator


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(
            first_name='user',
            last_name='test',
            email="test@gmail.com",
            phone_number='+380967564856',
            address='вулиця Проскурівська, 3, Хмельницький, Хмельницкая область, Украина',
            password='pzmY_9hm!crrD3X'
            )

    def test_token_activate_user(self):
        user = User.objects.get(pk=1)
        self.assertEquals(f'{six.text_type(user.pk)}{six.text_type("2001-1-1")}{six.text_type(user.is_active)}',
                          TokenGenerator()._make_hash_value(user, '2001-1-1')
                          )

