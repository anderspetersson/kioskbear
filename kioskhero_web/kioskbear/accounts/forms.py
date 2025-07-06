from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm
from django import forms
from .models import Account, Customer


class SignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full p-4 appearance-none border rounded-md shadow-sm placeholder-dark focus:outline-none focus:ring-brand focus:border-brand'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-4 appearance-none border rounded-md shadow-sm placeholder-dark focus:outline-none focus:ring-brand focus:border-brand'}))

    class Meta:
        model = Customer
        widgets = {
            'organisation_name': forms.TextInput(attrs={'class': 'w-full p-4 appearance-none border rounded-md shadow-sm placeholder-dark focus:outline-none focus:ring-brand focus:border-brand'})
        }
        fields = ('head_account', 'billing_account', 'organisation_name')

    def clean_email(self):
        if Account.objects.filter(email=self.cleaned_data.get("email")):
            raise forms.ValidationError(
                "Account with email %s already exist." % self.cleaned_data.get("email")
            )
        return self.cleaned_data.get("email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["head_account"].required = False
        self.fields["billing_account"].required = False


class SigninForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'w-full p-4 appearance-none border rounded-md shadow-sm placeholder-dark focus:outline-none focus:ring-brand focus:border-brand'
        self.fields['password'].widget.attrs['class'] = 'w-full p-4 appearance-none border rounded-md shadow-sm placeholder-dark focus:outline-none focus:ring-brand focus:border-brand'


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Account
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ("email",)

class PasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'w-full p-4 appearance-none border rounded-md shadow-sm placeholder-dark focus:outline-none focus:ring-brand focus:border-brand'
