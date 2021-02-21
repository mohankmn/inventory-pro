from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import math
import scipy.stats as st
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here

def validate_even(value):
    if value > 100 or value == 0:
        raise ValidationError(
            _('%(value)s is not in between 0 and 100 percent'),
            params={'value': value},
        )
def validate_zero(value):
    if value == 0:
        raise ValidationError(
            _('%(value)s cant be zero'),
            params={'value': value},
        )




class Items(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="items")
    name =models.CharField(max_length=150)
    lead_time=models.PositiveIntegerField(default='0',blank=True,null=True,validators=[validate_zero])
    service_level=models.PositiveIntegerField(default='0',blank=True,null=True,validators=[validate_even])
    standard_deviation=models.PositiveIntegerField(default='0',blank=True,null=True)
    carrying_cost=models.PositiveIntegerField(default='0',blank=False,validators=[validate_even],help_text='Enter as percentage of unit cost')
    ordering_cost=models.PositiveIntegerField(default='0',blank=False,null=True)
    unit_costprice=models.PositiveIntegerField(default='0',blank=False,null=True,validators=[validate_zero])
    average_daily_demand=models.PositiveIntegerField(default='0',blank=False,null=True)
    total_inventory=models.IntegerField(default='0',blank=True,null=True)
    eoq=models.IntegerField(default='0',blank=True,null=True)
    no_of_workingdays=models.IntegerField(default='0',blank=True,null=True)
    rq=models.IntegerField(default='0',blank=True,null=True)
    z=models.DecimalField(max_digits=4,decimal_places=3,default='0',blank=True,null=True)
 
    
    
    def __str__(self):
        return "{}".format(self.name)
    

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.eoq = math.sqrt((2*self.no_of_workingdays*self.average_daily_demand*self.ordering_cost)/(self.unit_costprice*(self.carrying_cost/100)))
        self.z=(st.norm.ppf(self.service_level/100))
        self.rq=(self.lead_time*self.average_daily_demand)+(self.z*self.standard_deviation*(self.lead_time))
        return super().save(*args, **kwargs)

    """def save(self,*args,**kwargs):
        self.z=int((st.norm.ppf(self.service_level/100)))*1000
        return super().save(*args, **kwargs)"""
    """def save(self,*args,**kwargs):
        self.lt=(math.sqrt(self.lead_time))*1000
        return super().save(*args, **kwargs)

    def save(self,*args,**kwargs):
        self.rq=(self.lead_time*self.average_daily_demand)+(self.z*self.standard_deviation*(self.lt))/1000000
        return super().save(*args, **kwargs)"""

    





class Demand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="demand")
    item=models.ForeignKey('Items', on_delete=models.CASCADE,related_name="demands")
    issue_quantity=models.IntegerField(blank=False,null=True)
    price=models.PositiveIntegerField(blank=False,null=True)
    recieve_quantity=models.IntegerField(default='0',blank=False,null=True)
    date=models.DateField(default=timezone.now,editable=True)


        
    
    def __str__(self):
        return "sold {} {} on {}".format(self.issue_quantity,self.item.name,self.date)
    


        



    