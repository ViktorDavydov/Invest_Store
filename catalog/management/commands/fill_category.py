from django.core.management import BaseCommand

from catalog.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        category_list = [
            {
                "pk": 1,
                "category_name": "Акции",
                "category_description": "Акции крупнейших компаний"
            },
            {
                "pk": 2,
                "category_name": "ПИФы",
                "category_description": "Паевые инвестиционные фонды"
            },
            {
                "pk": 3,
                "category_name": "Облигации",
                "category_description": "Корпоративные облигации"
            },
            {
                "pk": 4,
                "category_name": "БПИФ/ETF",
                "category_description": "Биржевые паевые инвестиционные фонды"
            }
        ]
        category_for_create = []
        for category_item in category_list:
            category_for_create.append(Category(**category_item))

        Category.objects.all().delete()
        Category.objects.bulk_create(category_for_create)
