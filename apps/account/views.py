from typing import Any, Union

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode

from django.views.generic import UpdateView, CreateView, TemplateView, FormView, ListView
from django.contrib.auth import get_user_model

from .forms import CustomUserChangeForm, CustomUserLoginForm, CustomRegistrationForm
from .tasks import send_activate_message
from .tokens import account_activation_token
from ..cart.models import Order


class UserChangeView(LoginRequiredMixin, UpdateView):
    """
    Displays and processes the change user page
    """
    template_name = 'registration/change_user.jinja2'
    form_class = CustomUserChangeForm

    def get_object(self, queryset=None) -> object:
        """return object of User for the current user"""
        return get_object_or_404(get_user_model(), pk=self.request.user.pk)

    def get_success_url(self) -> str:
        """return url address for personal area"""
        return reverse_lazy('personal-area')


class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Custom password change for users
    """
    template_name = 'registration/password_change.jinja2'
    form_class = PasswordChangeForm

    def get_object(self, queryset=None) -> object:
        """return object of User for the current user"""
        return get_object_or_404(get_user_model(), pk=self.request.user.pk)

    def get_success_url(self):
        """return url address for personal area"""
        return reverse_lazy('personal-area')


class CustomLoginView(LoginView):
    """Login view with form for create new user"""
    template_name = 'registration/login.jinja2'

    def get_context_data(self, *args, **kwargs) -> dict:
        """return form for login and create new user"""
        context = super(CustomLoginView, self).get_context_data(**kwargs)
        context['create_user_form'] = CustomUserLoginForm()
        return context


class UserCreateView(CreateView):
    """Displays and processes the new user page"""
    model = get_user_model()
    template_name = 'registration/create_user.jinja2'
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('confirm_registration')

    @transaction.atomic
    def form_valid(self, form: CustomRegistrationForm, *args: Any, **kwargs: dict) -> HttpResponseRedirect:
        """saves the user with the inactive status and sends an email message to confirm the identity"""
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_activate_message(user=user, request=self.request)
        return super(UserCreateView, self).form_valid(form)


class ActivateAccount(FormView):
    """Checks uidb64 and token for activate user"""

    def dispatch(self, request, *args, **kwargs) -> Union[HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse]:
        """Checks uidb64 and token for authenticity and, if successful, activates the user"""
        uidb64 = kwargs['uid']
        token = kwargs['token']
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except Exception:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('activate_done')
        else:
            return HttpResponse('Activation link is invalid!')


class ConfirmRegistrationView(TemplateView):
    """Displays a successful registration page"""
    template_name = 'registration/confirm_email_message_done.jinja2'


class PersonalArea(LoginRequiredMixin, ListView):
    """
    Personal area for current user
    """
    template_name = 'registration/profile.jinja2'

    def get_queryset(self):
        return Order.objects.filter(customer__email=self.request.user.email)
