from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        products_list = [
            {
                "pk": 1,
                "product_name": "IMOEX",
                "product_description": "Индекс Московской Биржи",
                "category": Category.objects.get(pk=1),
                "preview": "",
                "price": 3218,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            },
            {
                "pk": 2,
                "product_name": "Сбербанк",
                "product_description": "Сбербанк",
                "category": Category.objects.get(pk=1),
                "preview": "",
                "price": 283,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            },
            {
                "pk": 3,
                "product_name": "Лукойл",
                "product_description": "Лукойл",
                "category": Category.objects.get(pk=1),
                "preview": "",
                "price": 7200,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            },
            {
                "pk": 4,
                "product_name": "Накопительный резерв",
                "product_description": "ОПИФ Накопительный резерв",
                "category": Category.objects.get(pk=2),
                "preview": "",
                "price": 2888,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            },
            {
                "pk": 5,
                "product_name": "Российские Акции",
                "product_description": "ОПИФ БКС Российские Акции",
                "category": Category.objects.get(pk=2),
                "preview": "",
                "price": 513,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            },
            {
                "pk": 6,
                "product_name": "Капитал",
                "product_description": "ОПИФ БКС Капитал",
                "category": Category.objects.get(pk=2),
                "preview": "",
                "price": 624,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            },
            {
                "pk": 7,
                "product_name": "Сбербанк",
                "product_description": "Облигация Сбербанк",
                "category": Category.objects.get(pk=3),
                "preview": "",
                "price": 45,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            },
            {
                "pk": 8,
                "product_name": "ВТБ",
                "product_description": "Облигация Банк ВТБ",
                "category": Category.objects.get(pk=3),
                "preview": "",
                "price": 142,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            },
            {
                "pk": 9,
                "product_name": "СИБУР",
                "product_description": "Облигация СИБУР",
                "category": Category.objects.get(pk=3),
                "preview": "",
                "price": 23,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            },
            {
                "pk": 10,
                "product_name": "Ликвидность",
                "product_description": "БПИФ Ликвидность УК ВИМ",
                "category": Category.objects.get(pk=4),
                "preview": "",
                "price": 1,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            },
            {
                "pk": 11,
                "product_name": "Индекс МосБиржи",
                "product_description": "БПИФ Индекс МосБиржи УК ВИМ",
                "category": Category.objects.get(pk=4),
                "preview": "",
                "price": 141,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            },
            {
                "pk": 12,
                "product_name": "Золото",
                "product_description": "БПИФ Золото.Биржевой УК ВИМ",
                "category": Category.objects.get(pk=4),
                "preview": "",
                "price": 2,
                "create_date": "2000-01-01",
                "final_change_date": "2023-11-21"
            }
        ]
        category_for_create = []
        for product_item in products_list:
            category_for_create.append(Product(**product_item))

        Product.objects.all().delete()
        Product.objects.bulk_create(category_for_create)
