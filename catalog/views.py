from django.shortcuts import render
import json
from catalog.models import Product, Contacts


def index(request):
    print(Product.objects.all()[:5])  # 1-е задание со *. Вообще правильно ли я его понял?
    return render(request, 'catalog/index.html')


def contacts(request):
    all_contacts = Contacts.objects.all()
    if request.method == 'POST':
        contact_dict = {
            "Имя": request.POST.get('name'),
            "Почта": request.POST.get('email'),
            "Сообщение": request.POST.get('message')
        }
        with open("contacts.json", 'a', encoding='UTF-8') as f:
            json.dump(contact_dict, f, indent=2, ensure_ascii=False)
    return render(request, 'catalog/contacts.html', locals())
