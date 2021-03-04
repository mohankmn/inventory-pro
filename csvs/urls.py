from django.urls import path
from .views import upload_file_view, upload_product_file_view

app_name = 'csvs'

urlpatterns = [
    path('purchase/', upload_file_view, name='upload-view'),
    path('product/', upload_product_file_view, name='upload-view-product'),
]