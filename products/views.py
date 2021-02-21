from django.shortcuts import render
from .models import Product, Purchase
import pandas as pd
from .utils import get_simple_plot, get_salesman_from_id, get_image
from .forms import PurchaseForm
from django.http import HttpResponse
import matplotlib.pyplot as plt
import seaborn as sns
# Create your views here.

def sales_dist_view(request):
    df = pd.DataFrame(Purchase.objects.all().values())
    df['salesman_id']=df['salesman_id'].apply(get_salesman_from_id)
    df.rename({'salesman_id':'salesman'}, axis=1, inplace=True)
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    plt.switch_backend('Agg')
    plt.xticks(rotation=90)
    sns.barplot(x='date', y='total_price', hue='salesman', data=df)
    plt.tight_layout
    graph = get_image()

    #return HttpResponse("Hello Salesman")
    return render(request, 'products/sales.html', {'graph':graph})

def chart_select_view(request):
    error_message = None
    df = None
    graph = None
    price = None

    product_df = pd.DataFrame(Product.objects.all().values())
    purchase_df = pd.DataFrame(Purchase.objects.all().values())
    if product_df.shape[0]>0 :
        product_df['product_id'] = product_df['id']
    
    if purchase_df.shape[0]>0 :
        df = pd.merge(purchase_df, product_df, on='product_id').drop(['id_y', 'date_y'], axis=1).rename({'id_x':'id', 'date_x':'date'}, axis=1)
        price = df['price']
        if request.method == 'POST':
            chart_type = request.POST.get('sales')
            date_from  = request.POST.get('date_from') 
            date_to    = request.POST.get('date_to')

            df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
            df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')

            if chart_type!="":
                if date_from!="" and date_to!="":
                    df = df[(df['date']>date_from)&(df['date']<date_to)]
                    df2 = df.groupby('date', as_index=False)['total_price'].agg('sum')
                # function to get a graph
                graph = get_simple_plot(chart_type, x=df2['date'], y=df2['total_price'] ,data=df)
            else:
                error_message = 'please select a chart to continue'

    else:
        error_message = 'no records in database'
        
    context ={
        'error_message': error_message,
        'graph' : graph,
        'price' : price,
        #'products' : product_df.to_html(),
        #'purchase' : purchase_df.to_html(),
        #'df'       : df,
    }
    return render(request, 'products/main.html', context)

def add_purchase_view(request):
    form = PurchaseForm(request.POST or None)
    added_message = None

    if form.is_valid():
        obj = form.save(commit=False)
        obj.salesman = request.user
        obj.save()

        form = PurchaseForm()
        added_message = 'The purchase has been added'

    context = {
        'form' : form,
        'added_message' : added_message,
    }
    return render(request, 'products/add.html', context)