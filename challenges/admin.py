from django.contrib import admin
from tinymce import TinyMCE
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
    fieldsets = (None, {'fields': ('text',)}),
    can_delete = True


class AttachmentAdmin(admin.TabularInline):
    model = Attachment
    fieldsets = (None, {'fields': ('name', 'description', 'file')}),
    can_delete = True


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    form = ChallengeAdminForm
    inlines = (HintAdmin, AttachmentAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm


@admin.register(ChallengeSolved)
class ChallengeSolvedAdmin(admin.ModelAdmin):
    pass

