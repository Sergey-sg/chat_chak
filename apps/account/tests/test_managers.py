from django.test import TestCase

from apps.account.models import User


class UserModelTest(TestCase):

    def test_create_user(self):
        User.objects.create_user(
            email="test@gmail.com",
            password='pzmY_9hm!crrD3X',
        )
        self.assertEquals(User.objects.get(pk=1).email, "test@gmail.com")

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='pzmY_9hm!crrD3X')

    def test_create_superuser(self):
        User.objects.create_superuser(
            email="test@gmail.com",
            password='pzmY_9hm!crrD3X',
        )
        self.assertEquals(User.objects.get(pk=1).email, "test@gmail.com")
        self.assertTrue(User.objects.get(pk=1).is_staff)
        self.assertTrue(User.objects.get(pk=1).is_superuser)
        self.assertTrue(User.objects.get(pk=1).is_active)

    def test_create_superuser_without_is_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=None,
                password='pzmY_9hm!crrD3X',
                is_staff=False,
            )

    def test_create_superuser_without_is_superuser(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=None,
                password='pzmY_9hm!crrD3X',
                is_superuser=False,
            )
