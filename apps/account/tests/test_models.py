from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.account.models import User


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

    def test_str_method(self):
        user = User.objects.get(pk=1)
        field_email = user.email
        self.assertEquals(field_email, user.__str__())

    def test_load_photo(self):
        user = User.objects.get(pk=1)
        photo = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('static/media/user_photo/default_user_photo.png', 'rb').read(),
            content_type='image/jpeg'
        )
        user.photo = photo
        user.save()
        self.assertIn(user.email.replace('@', ''), user.photo.name)
        self.assertEquals(user.img_alt, f'photo {user.email} user')
