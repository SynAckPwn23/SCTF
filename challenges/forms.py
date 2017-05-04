from django import forms

from .models import Category, Hint

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)



class HintForm(forms.ModelForm):

    class Meta:
        model = Hint
        fields = ('text',)
