from django.shortcuts import render, redirect
from .forms import CsvForm
from .models import Csv
import csv
import math
from django.contrib.auth.models import User
from products.models import Product, Purchase
from products.forms import *
from products.views import ItemCreate

# Create your views here.

def upload_file_view(request):
    error_message   = None
    success_message = None
    form = CsvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvForm()
        try:
            obj = Csv.objects.get(activated=False)
            with open(obj.file_name.path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    user = request.user
                    prod = Product.objects.get(name=row[0].upper())
                    Purchase.objects.create(
                        product = prod,
                        price = int(row[2]),
                        quantity = int(row[1]),
                        user = user,
                        date = row[4],
                    )
            
            obj.activated=True
            obj.save()
            success_message = 'successfully uploaded.'

        except:
            error_message = 'Oops, something went wrong......'

    context={
        'form' : form,
        'error_message' : error_message,
        'success_message' : success_message,
    }
    return render(request, 'csvs/upload.html', context)

    


def upload_product_file_view(request):
    error_message   = None
    success_message = None
    form = CsvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvForm() 
        try:
            obj = Csv.objects.get(activated=False)
            with open(obj.file_name.path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    try:
                        prod = Product.objects.get(name=row[0].upper())
                    except:
                        Product.objects.create(
                            user                 = request.user,
                            name                 = row[0].upper(),
                            date                 = row[1],
                            average_daily_demand = int(row[2]),
                            standard_deviation   = int(row[3]),
                            carrying_cost        = int(row[4]),
                            ordering_cost        = int(row[5]),
                            unit_costprice       = int(row[6]),
                            total_inventory      = int(row[7]),
                            lead_time            = int(row[8]),
                            service_level        = int('90'),
                            no_of_workingdays    = int('300'),
                            z                    = float('1.28'),
                            eoq       = math.sqrt(2*300*float(row[2])*float(row[5]))/(float(row[6])*float(row[4])/100),
                            rq        = (float(row[8])*float(row[2]))+(1.28*float(row[3])*float(row[8])),
                        )
            obj.activated=True
            obj.save()
            success_message = 'successfully uploaded.'
        except:
            error_message = 'Oops, something went wrong......'

    context={
        'form' : form,
        'error_message' : error_message,
        'success_message' : success_message,
    }
    return render(request, 'csvs/upload_product.html', context)