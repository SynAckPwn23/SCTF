from django.contrib import admin

from challenges.forms import HintForm
from challenges.models import Challenge, Category, Hint, Attachment, ChallengeSolved


class HintAdmin(admin.TabularInline):
    model = Hint
    form = HintForm
    can_delete = True


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    inlines = (HintAdmin,)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ChallengeSolved)
class ChallengeSolvedAdmin(admin.ModelAdmin):
    pass
