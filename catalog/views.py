from django.shortcuts import render
import json


def index(request):
    return render(request, 'catalog/index.html')


def contacts(request):
    if request.method == 'POST':
        contact_dict = {
            "Имя": request.POST.get('name'),
            "Почта": request.POST.get('email'),
            "Сообщение": request.POST.get('message')
        }
        with open("contacts.json", 'a', encoding='UTF-8') as f:
            json.dump(contact_dict, f, indent=2, ensure_ascii=False)
    return render(request, 'catalog/contacts.html')
