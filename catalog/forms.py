from django import forms
from django.forms import BaseInlineFormSet

from catalog.models import Product, Blog


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_active' or field_name == 'is_published':
                field.widget.attrs['class'] = 'form'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('owner',)

    def clean_product_name(self):
        cleaned_data = self.cleaned_data.get('product_name', )
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                           'обман', 'полиция', 'радар']
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Использовано запрещенное слово')
        return cleaned_data

    def clean_product_description(self):
        cleaned_data = self.cleaned_data.get('product_description')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                           'обман', 'полиция', 'радар']
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Использовано запрещенное слово')
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('prod',)


class VersionBaseInLineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        active_list = [form.cleaned_data['is_active'] for form in self.forms if
                       'is_active' in form.cleaned_data]
        if active_list.count(True) > 1:
            raise forms.ValidationError('ОШИБКА! Только одна версия может быть активна')


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('slug', 'views_count')


class ModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('product_name', 'preview', 'price', 'create_date', 'final_change_date', 'owner')
