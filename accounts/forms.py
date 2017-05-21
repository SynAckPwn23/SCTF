from django import forms
from django.forms.models import ModelForm
from registration.forms import RegistrationForm
from tinymce import TinyMCE

from accounts.models import UserProfile
from challenges.models import Challenge, Category


class CustomRegistrationForm(RegistrationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = RegistrationForm.Meta.model
        fields = RegistrationForm.Meta.fields + ['first_name', 'last_name']


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'team']



class ChallengeAdminForm(forms.ModelForm):
    class Meta:
        model = Challenge
        widgets = {
           'description': TinyMCE(mce_attrs={'width': 800})
        }
        fields = '__all__'


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        widgets = {
           'description': TinyMCE(mce_attrs={'width': 800})
        }
        fields = '__all__'
