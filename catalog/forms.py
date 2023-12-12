from django import forms

from catalog.models import Product


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('vers',)

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
        fields = '__all__'

    def clean_prod(self):
        cleaned_data = super().clean()
        product = self.instance.product
        is_active = cleaned_data.get('is_active')
        if is_active and product.versions.filter(is_active=True).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError('Только одна версия может быть активной')
