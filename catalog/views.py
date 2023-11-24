from django.shortcuts import render
import json
from catalog.models import Product, Contacts, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    objects_list = Product.objects.all()
    # context = {
    #     'objects_list': objects_list,
    #     'title': 'Каталог'
    # }
    paginator = Paginator(objects_list, 3)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    temps = {
        'products': products
    }

    return render(request, 'catalog/index.html', temps)


def contacts(request):
    all_contacts = Contacts.objects.all()
    context = {
        'title': 'Контакты'
    }
    if request.method == 'POST':
        contact_dict = {
            "Имя": request.POST.get('name'),
            "Почта": request.POST.get('email'),
            "Сообщение": request.POST.get('message')
        }
        with open("contacts.json", 'a', encoding='UTF-8') as f:
            json.dump(contact_dict, f, indent=2, ensure_ascii=False)
    return render(request, 'catalog/contacts.html', locals())


def product(request, pk):
    chosen_product = Product.objects.get(pk=pk)
    context = {
        'chosen_product': chosen_product,
    }
    return render(request, 'catalog/product.html', context)


def add_product(request):
    category_list = Category.objects.all()
    context = {
        'category_list': category_list
    }
    if request.method == "POST":

        product_information = {
            "id": 14,
            "product_name": request.POST.get('name'),
            "product_description": request.POST.get('description'),
            "category": request.POST.get('category'),
            "preview": request.POST.get('preview'),
            "price": request.POST.get('price'),
            "create_date": "2000-01-01",
            "final_change_date": "2023-11-25"
        }
        # products_for_create = [Product(**product_information)]
        # Product.objects.bulk_create(products_for_create)
        print(product_information)
    return render(request, 'catalog/add_product.html', context)
