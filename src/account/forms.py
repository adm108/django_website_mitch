from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=60,
                             help_text="Required. Add a valid email address")

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')


class AccountAuthenticatedForm(forms.ModelForm):

    # label - password does not show the letters
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    # clean method checking if data is valid, if not it will clean form
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid login')


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'username')

    def clean_email(self):
        # it cleans forms if something is wrong and checking errors
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(
                    email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError(f'Email {account.email} is already in use.')

    def clean_username(self):
        # it cleans forms if something is wrong and checking errors
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError(f'Username {account.username} is already in '
                                        f'use.')
