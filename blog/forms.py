from django import forms

class PostForm(forms.Form):
    title = forms.CharField(required=True)
    summary = forms.TextField(required=True)
    text = forms.TextField(required=True)

class CommentForm(forms.Form):
    text = forms.TextField(required=True)