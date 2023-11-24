from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, contacts, product, add_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:pk>', product, name='product'),
    path('add_product/', add_product, name='add_product'),

]
