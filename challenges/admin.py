from django.contrib import admin
from django import forms
from redactor.widgets import RedactorEditor
from tinymce import TinyMCE

from challenges.forms import HintForm
from challenges.models import Challenge, Category, Hint, Attachment, ChallengeSolved


class HintAdmin(admin.TabularInline):
    model = Hint
    form = HintForm
    can_delete = True


class ChallengeAdminForm(forms.ModelForm):
    class Meta:
        model = Challenge
        widgets = {
           'description': TinyMCE(mce_attrs={'width': 800})
        }
        fields = '__all__'


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    inlines = (HintAdmin,)
    form = ChallengeAdminForm


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ChallengeSolved)
class ChallengeSolvedAdmin(admin.ModelAdmin):
    pass

