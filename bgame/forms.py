from django import forms

from .models import Comment, WantPlay, Interest


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("content", "bgame", "user")

        widgets = {
            "bgame": forms.HiddenInput(),
            "user": forms.HiddenInput()
        }

        labels = {
            "content": "コメントを入力"
        }




class WantPlayForm(forms.ModelForm):

    class Meta:
        model = WantPlay
        fields = ("user", "bgame")

        widgets = {
            "user": forms.HiddenInput(),
            "bgame": forms.HiddenInput()
        }




class InterestForm(forms.ModelForm):

    class Meta:
        model = Interest
        fields = ("user", "bgame")

        widgets = {
            "user": forms.HiddenInput(),
            "bgame": forms.HiddenInput()
        }