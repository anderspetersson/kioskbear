from django.views.generic import CreateView, TemplateView, View
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.shortcuts import redirect

from kioskbear.kiosk.models import Survey, Block
from kioskbear.feedback.models import ScoredOption

from .models import Customer, Account
from .forms import SignupForm
from .utils import email_verification_token


class SignupView(CreateView):
    model = Customer
    form_class = SignupForm
    template_name = 'landingpages/accounts/signup.html'

    def form_valid(self, form):
        customer = form.save(commit=False)
        account = Account.objects.create_user(
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password')
        )

        customer.head_account = account
        customer.billing_account = account
        customer.save()

        account.customer = customer
        account.save()

        self._send_email_verification(account)

        return super().form_valid(form)

    def _send_email_verification(self, user: Account):
        subject = 'Activate Your Kioskbear Account'
        body = render_to_string(
            'emails/email_verification.html',
            {
                'domain': self.request.get_host(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            }
        )
        EmailMessage(to=[user.email], subject=subject, body=body).send()

    def get_success_url(self):
        return reverse_lazy('accounts:signup-success')


class ActivateAccountView(View):
    def get_user_from_email_verification_token(self, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                Account.DoesNotExist):
            return None

        if user is not None and email_verification_token.check_token(user, token):
            return user

        return None

    def get(self, request, uidb64, token):
        user = self.get_user_from_email_verification_token(uidb64, token)
        user.is_active = True
        user.save()

        survey = Survey.objects.create(customer=user.customer)
        start_block = Block.objects.create(
            title='How would you rate us based on todays visit?',
            survey=survey
        )
        data = [
            {'emoji': '🤬', 'score': 1},
            {'emoji': '🤨', 'score': 2},
            {'emoji': '🙂', 'score': 3},
            {'emoji': '😀', 'score': 4},
            {'emoji': '😍', 'score': 5}
        ]

        for i in data:
            ScoredOption.objects.create(text=i['emoji'], score=i['score'], block=start_block)

        end_block = Block.objects.create(
            title='Thanks for the feedback!',
            survey=survey
        )

        survey.start_block = start_block
        survey.end_block = end_block
        survey.save()

        login(request, user)
        return redirect('app:dashboard')


class SignupSuccessWaitingForAccountActivationView(TemplateView):
    template_name = 'landingpages/accounts/signup_success_waiting_for_account_activation.html'
