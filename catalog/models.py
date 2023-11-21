from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    category_name = models.CharField(max_length=30, verbose_name='наименование категории')
    category_description = models.CharField(max_length=100, verbose_name='описание категории')

    def __str__(self):
        return f'{self.category_name} - {self.category_description}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('category_name',)


class Product(models.Model):
    product_name = models.CharField(max_length=30, verbose_name='наименование товара')
    product_description = models.CharField(max_length=100, verbose_name='описание товара')
    preview = models.ImageField(upload_to='products/', verbose_name='превью', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 max_length=20, verbose_name='наименование категории')
    price = models.IntegerField(verbose_name='цена за покупку')
    create_date = models.DateField(auto_now=False, auto_now_add=False,
                                   verbose_name='дата создания')
    final_change_date = models.DateField(auto_now=False, auto_now_add=False,
                                         verbose_name='дата последнего изменения')

    def __str__(self):
        return f"{self.product_name}"

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('product_name',)
