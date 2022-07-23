from django import forms
from django.forms import ModelForm
from .models import *

class CreateListing(ModelForm):
    class Meta:
        model = Listing
        fields = ["item", "description", "image", "category", "price"]

        widget = {
            'item': forms.TextInput(attrs={'class':'create__item'}),
            'description': forms.TextInput(attrs={'class':'create__item'}),
            'image': forms.ClearableFileInput(attrs={'class':'create__item'}),
            'category': forms.Select(attrs={'class':'create__item'}),
            'item': forms.TextInput(attrs={'class':'create__item'}),
            'price': forms.NumberInput(attrs={'class':'create__item'})
        }

class CreateBid(ModelForm):
    class Meta:
        model = Bids
        fields = ["bid"]
        labels = {
            "bid": ""
        }

        widget = {
            'bid': forms.NumberInput(attrs={'class':'bid__item'})
        }



class CreateComment(ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]
        labels = {
            "comment": ""
        }
        widget = {
            "comment": forms.TextInput(attrs={"class":"comment__comment", "placeholder": "Leave a comment"}),
        }