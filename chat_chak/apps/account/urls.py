from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include
from django.views.generic import TemplateView

from apps.account.views import CustomLoginView, UserCreateView, PersonalArea, UserChangeView, MyPasswordChangeView, \
    ConfirmRegistrationView, ActivateAccount


urlpatterns = [
    path('', PersonalArea.as_view(), name='personal-area'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.jinja2'), name='logout'),
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('activate-done/', TemplateView.as_view(
        template_name='registration/activate_done.jinja2'), name='activate_done'),
    path('change/', UserChangeView.as_view(), name='user-change'),
    path('password/', include([
        path('', MyPasswordChangeView.as_view(), name='password-change'),
        path('reset/', include([
            path('', PasswordResetView.as_view(template_name='registration/password_reset_form.jinja2'),
                 name='password_reset'),
            path('done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.jinja2'),
                 name='password_reset_done'),
            path('<uidb64>/<token>/',
                 PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.jinja2"),
                 name='password_reset_confirm'
                 ),
            path('complete/', PasswordResetCompleteView.as_view(
                template_name='registration/password_reset_complete.jinja2'), name='password_reset_complete'),
        ])),
    ])),

    path('confirmregistration/', ConfirmRegistrationView.as_view(), name='confirm_registration'),
    path('activate/<uid>/<token>/', ActivateAccount.as_view(), name='user_activate')
]
