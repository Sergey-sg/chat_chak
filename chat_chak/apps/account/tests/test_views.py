from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.account.forms import CustomUserLoginForm
from apps.account.models import User
from apps.account.tokens import account_activation_token
from apps.account.views import MyPasswordChangeView, CustomLoginView
from apps.cart.models import Order, Customer


class UserChangeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create_user(
            email="test@gmail.com",
            password='pzmY_9hm!crrD3X'
        )
        user = User.objects.get(pk=1)
        user.first_name = 'user'
        user.last_name = 'test'
        user.phone_number = '+380967564856'
        user.address = 'вулиця Проскурівська, 3, Хмельницький, Хмельницкая область, Украина'
        user.save()

    def test_UserChangeView(self):
        # not login
        resp = self.client.get(reverse_lazy('user-change'))
        self.assertEqual(resp.url, f'{reverse_lazy("login")}?next={reverse_lazy("user-change")}')
        # login
        self.client.login(email="test@gmail.com", password='pzmY_9hm!crrD3X')
        resp = self.client.get(reverse_lazy('user-change'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(reverse_lazy('user-change'))
        self.assertEqual(resp.url, reverse_lazy('personal-area'))

    def test_MyPasswordChangeView(self):
        # not login
        resp = self.client.get(reverse_lazy('password-change'))
        self.assertEqual(resp.url, f'{reverse_lazy("login")}?next={reverse_lazy("password-change")}')
        # login
        self.client.login(email="test@gmail.com", password='pzmY_9hm!crrD3X')
        resp = self.client.get(reverse_lazy('password-change'))
        self.assertEqual(resp.status_code, 200)
        # test get_object()
        user = User.objects.get(pk=1)
        request = RequestFactory().get(reverse_lazy('password-change'))
        request.user = user
        my_view = MyPasswordChangeView()
        my_view.setup(request)
        self.assertEqual(user, my_view.get_object())
        # test get_success_url()
        resp = self.client.post(
            reverse_lazy('password-change'),
            data={
                'old_password': 'pzmY_9hm!crrD3X',
                'new_password1': 'pzmY_9hm!crrD3X',
                'new_password2': 'pzmY_9hm!crrD3X'
            }
        )
        self.assertEqual(resp.url, reverse_lazy('personal-area'))

    def test_CustomLoginView(self):
        # test get_context_data()
        request = RequestFactory().get(reverse_lazy('login'))
        my_view = CustomLoginView()
        my_view.setup(request)
        form = CustomUserLoginForm()
        self.assertEqual(f'{form}', f'{my_view.get_context_data()["create_user_form"]}')

    def test_UserCreateView(self):
        # form_valid
        resp = self.client.get(reverse_lazy('create_user'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            reverse_lazy('create_user'),
            data={'email': 'test@create.com',
                  'password1': 'pzmY_9hm!crrD3X',
                  'password2': 'pzmY_9hm!crrD3X'
                  }
        )
        self.assertEqual(resp.url, reverse_lazy('confirm_registration'))
        self.assertEqual('test@create.com', User.objects.get(pk=2).email)

    def test_ActivateAccount(self):
        user = User.objects.get(pk=1)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        resp = self.client.get(reverse_lazy('user_activate', kwargs={'uid': uid, 'token': token}))
        self.assertRedirects(resp, reverse_lazy('activate_done'))
        # test user = None
        uid = urlsafe_base64_encode(force_bytes(2)),
        token = account_activation_token.make_token(user),
        resp = self.client.get(reverse_lazy('user_activate', kwargs={'uid': uid, 'token': token}))
        self.assertEqual(resp.status_code, 200)

    def test_PersonalArea(self):
        customer = Customer.objects.create(
            name='customer',
            email='test@gmail.com',
            phone='+380678574738',
            address='Запорожье, Запорожская область, Украина',
            geolocation='47.8388,35.139567'
            )
        Order.objects.create(customer=customer, total_price=34.5)
        # not login
        resp = self.client.get(reverse_lazy('personal-area'))
        self.assertRedirects(resp, f'{reverse_lazy("login")}?next={reverse_lazy("personal-area")}')
        # login
        self.client.login(email="test@gmail.com", password='pzmY_9hm!crrD3X')
        resp = self.client.get(reverse_lazy('personal-area'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context['object_list']),
            list(Order.objects.filter(customer__email=User.objects.get(pk=1)))
        )
