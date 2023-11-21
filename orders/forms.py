from django import forms

from orders.models import PreOrder


class PreOrderForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputColumn2', 'placeholder': 'Name'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputColumn2', 'placeholder': 'Surname'}))
    phoneNumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputColumn1', 'placeholder': 'phoneNumber'}))
    agent = forms.CharField(widget=forms.TextInput(attrs={'class': 'inputColumn1', 'placeholder': 'Agent'}))

    class Meta:
        model = PreOrder
        fields = ('name', 'surname', 'phoneNumber', 'agent')
