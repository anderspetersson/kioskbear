from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .views import SignupView, ActivateAccountView, SignupSuccessWaitingForAccountActivationView
from .forms import SigninForm, PasswordResetForm

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', auth_views.LoginView.as_view(template_name='landingpages/accounts/signin.html', authentication_form=SigninForm), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='signout'),
    path('signup/success/', SignupSuccessWaitingForAccountActivationView.as_view(), name='signup-success'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='landingpages/accounts/password_reset.html', email_template_name='emails/password_reset.html', form_class=PasswordResetForm, success_url=reverse_lazy('accounts:password_reset_done')), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='landingpages/accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='landingpages/accounts/password_choose_new.html', success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='landingpages/accounts/password_reset_complete.html'), name='password_reset_complete'),
]