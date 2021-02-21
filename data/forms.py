
from os import name
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.http import request

from .models import Items,Demand


class ItemsForm(forms.ModelForm):
    class Meta:
        model =Items
        fields=['name','average_daily_demand','unit_costprice','carrying_cost','ordering_cost','total_inventory','lead_time','service_level','standard_deviation','no_of_workingdays']
    def clean_name(self):
      name=self.cleaned_data.get('name').upper()

      """if not name:
        raise forms.ValidationError('Fill This Field')
      for i in Items.objects.all():
        if i.name == name:
          raise forms.ValidationError(name + '  is already exists')"""
      return name

class DemandForm(forms.ModelForm):
  class Meta:
    model=Demand
    fields='__all__'
    exclude={'user'}
  def __init__(self,user=None,*args,**kwargs):
    super(DemandForm,self).__init__(*args,**kwargs)
    if user:
      self.fields['item'].queryset=Items.objects.filter(user=user)
class ItemSearchForm(forms.ModelForm):
   class Meta:
     model = Items
     fields = ['name']
"""class IssueForm(forms.ModelForm):
  class Meta:
    model=Demand
    fields=['issue_quantity','price']"""








#title.widget.attrs.update({'class':'form-control'})
#slug.widget.attrs.update({'class':'form-control'})

#def clean_slug(self):
#new_slug=self.cleaned_data.get('name').lower()
#if new_slug=='create':
#raise ValidationError ('slug may not be created')
#return new_slug

    