from django import forms
from .models import PostComment

class PostCommentForm(forms.Form):
    post_id = forms.IntegerField(
        required=True,
        min_value=1,
    )
    email = forms.EmailField(required=True)
    name = forms.CharField(
        required=True, 
        max_length=200
    )
    comment = forms.CharField(
        required=True, 
        min_length=1
    )