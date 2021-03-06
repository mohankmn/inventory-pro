from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import math
import scipy.stats as st
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# validation

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

# Create your models here.

class Product(models.Model):
    user                 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="items")
    name                 = models.CharField(max_length=220)
    date                 = models.DateTimeField(auto_now_add=True)
    lead_time            = models.PositiveIntegerField(default='0',blank=True,null=True,validators=[validate_zero])
    service_level        = models.PositiveIntegerField(default='90',blank=True,null=True,validators=[validate_even])
    standard_deviation   = models.PositiveIntegerField(default='5',blank=True,null=True)
    carrying_cost        = models.PositiveIntegerField(default='12',blank=False,validators=[validate_even],help_text='Enter as percentage of unit cost')
    ordering_cost        = models.PositiveIntegerField(default='0',blank=False,null=True)
    unit_costprice       = models.PositiveIntegerField(default='0',blank=False,null=True,validators=[validate_zero])
    average_daily_demand = models.PositiveIntegerField(default='0',blank=False,null=True)
    total_inventory      = models.IntegerField(default='0',blank=True,null=True)
    eoq                  = models.IntegerField(default='0',blank=True,null=True)
    no_of_workingdays    = models.IntegerField(default='300',blank=True,null=True)
    rq                   = models.IntegerField(default='0',blank=True,null=True)
    z                    = models.DecimalField(max_digits=4,decimal_places=3,default='0',blank=True,null=True)

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        a = 2*float(self.no_of_workingdays)*float(self.average_daily_demand)*float(self.ordering_cost)
        b = float(self.unit_costprice)*float(self.carrying_cost)/100
        self.eoq  = math.sqrt(a/b)
        self.z    = (st.norm.ppf(self.service_level/100))
        self.rq   = (self.lead_time*self.average_daily_demand)+(self.z*self.standard_deviation*(self.lead_time))
        return super().save(*args, **kwargs)

class Purchase(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name="demand")
    product     = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="demands")
    price       = models.PositiveIntegerField(blank=False,null=True)
    quantity    = models.IntegerField(blank=False,null=True)
    total_price = models.PositiveIntegerField(blank=True)
    date        = models.DateTimeField(default=timezone.now, editable=True)    
    recieved    = models.IntegerField(default='0',blank=False,null=True)


    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return "sold {} - {} items for {}".format(self.product.name, self.quantity, self.total_price)

