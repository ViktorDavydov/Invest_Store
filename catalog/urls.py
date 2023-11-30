from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductDetailView, ProductListView, \
    ContactsCreateView, ProductCreateView, BlogListView, BlogCreateView, BlogDetailView, \
    BlogUpdateView, BlogDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('contacts/', ContactsCreateView.as_view(), name='create_contacts'),
    path('view/<int:pk>', ProductDetailView.as_view(), name='view'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('article_create/', BlogCreateView.as_view(), name='article_create'),
    path('blog/article/<int:pk>', BlogDetailView.as_view(), name='article'),
    path('blog/edit/<int:pk>', BlogUpdateView.as_view(), name='update_article'),
    path('blog/delete/<int:pk>', BlogDeleteView.as_view(), name='delete_article'),

]
