from django.contrib import admin
from tinymce import TinyMCE

from challenges.forms import HintForm
from challenges.models import Hint, Attachment, ChallengeSolved, Challenge, Category
from django import forms


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


class HintAdmin(admin.TabularInline):
    model = Hint
    form = HintForm
    can_delete = True


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    inlines = (HintAdmin,)
    form = ChallengeAdminForm


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm


@admin.register(ChallengeSolved)
class ChallengeSolvedAdmin(admin.ModelAdmin):
    pass

