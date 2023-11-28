from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductDetailView, ProductListView, \
    ContactsCreateView, ProductCreateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('contacts/', ContactsCreateView.as_view(), name='create_contacts'),
    path('view/<int:pk>', ProductDetailView.as_view(), name='view'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),

]
