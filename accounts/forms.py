from django import forms
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
import django.forms.models as models
from registration.forms import RegistrationForm

from accounts.models import UserProfile, UserTeamRequest, Team
from accounts.utils import user_without_team


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


class TeamCreateForm(ModelForm):

    def save(self, commit=True):
        team = super(TeamCreateForm, self).save(commit=commit)
        team.created_by.profile.team = team
        team.created_by.profile.save()
        return team

    class Meta:
        model = Team
        fields = ['name', 'created_by']


class UserTeamRequestCreateForm(ModelForm):
    class Meta:
        model = UserTeamRequest
        fields = ['user', 'team']