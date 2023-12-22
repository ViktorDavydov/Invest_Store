from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from catalog.views import ProductDetailView, ProductListView, \
    ContactsCreateView, ProductCreateView, BlogListView, BlogCreateView, BlogDetailView, \
    BlogUpdateView, BlogDeleteView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('contacts/', never_cache(ContactsCreateView.as_view()), name='create_contacts'),
    path('view/<int:pk>', ProductDetailView.as_view(), name='view'),
    path('create_product/', never_cache(ProductCreateView.as_view()), name='create_product'),
    path('edit_product/<int:pk>', never_cache(ProductUpdateView.as_view()), name='edit_product'),
    path('delete_product/<int:pk>', ProductDeleteView.as_view(), name='delete_product'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('article_create/', never_cache(BlogCreateView.as_view()), name='article_create'),
    path('blog/article/<slug>', BlogDetailView.as_view(), name='article'),
    path('blog/edit/<slug>', never_cache(BlogUpdateView.as_view()), name='update_article'),
    path('blog/delete/<slug>', BlogDeleteView.as_view(), name='delete_article'),

]
