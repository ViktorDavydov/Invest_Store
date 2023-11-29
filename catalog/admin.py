from django.contrib import admin

from catalog.models import Category, Product, Contacts, Blog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'category_description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('product_name', 'product_description',)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('contact_name', 'contact_email',)


@admin.register(Blog)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('article_name', 'slug',)
