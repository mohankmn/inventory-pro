from django import forms
from .models import Purchase, Product

class PurchaseForm(forms.ModelForm):
    # to style the product button, but it is ok with out this for our form
    #product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Product',
                                     #widget=forms.Select(attrs={'class':'ui selection dropdown'}))
    class Meta:
        model = Purchase
        fields = ['product','price','quantity']