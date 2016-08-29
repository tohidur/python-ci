from django import forms
from .models import Collection, Link, Tag


class CollectionForm(forms.ModelForm):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Board Name'}))
    description = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-input',
     'placeholder': 'Small Descriptiono (Optional)', 'rows': 2, 'cols': 100}), required=False)
    privacy = forms.BooleanField(label='Make it a private board.', required=False)
    class Meta:
        model = Collection
        fields = [
            "title",
            "description",
            "privacy",
        ]


class LinkForm(forms.ModelForm):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Title (Optional)'}))
    link = forms.URLField(label="", widget=forms.TextInput(attrs={'placeholder': 'http://www.yourlink.com'}), required=True)
    tags = forms.ModelMultipleChoiceField(label="*Write custom tags and hit enter to attach", queryset=Tag.objects.all())
    class Meta:
        model = Link
        fields = [
            "title",
            "link",
            "tags",
        ]