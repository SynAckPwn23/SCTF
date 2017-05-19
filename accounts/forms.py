from django import forms
from django.forms.models import ModelForm
from registration.forms import RegistrationForm

from accounts.models import UserProfile


class CustomRegistrationForm(RegistrationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = RegistrationForm.Meta.model
        fields = RegistrationForm.Meta.fields + ['first_name', 'last_name']


class UserProfileForm(ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['image']