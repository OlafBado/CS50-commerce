from django import forms
from .models import Comments

class NewCommentForm(forms.ModelForm):

    #rapid form development
    class Meta:
        #model to use
        model = Comments
        #what fields to use
        fields = ("name", "email", "content")
        #additional, inject class to input forms
        widgets = {
            "name": forms.TextInput(attrs={"class": "col-sm-12"}),
            "email": forms.TextInput(attrs={"class": "col-sm-12"}),
            "content": forms.Textarea(attrs={"class": "form-control"})
        }