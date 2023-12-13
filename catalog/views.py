import json

from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Contacts, Category, Blog, Version
from config import settings


class ContactsCreateView(CreateView):
    model = Contacts
    fields = ('contact_name', 'contact_email',)
    success_url = reverse_lazy('catalog:create_contacts')

    def form_valid(self, form):
        if form.is_valid():
            new_contact = form.save()
            new_contact.personal_manager = self.request.user
            new_contact.save()
            contact_dict = {
                "Имя": new_contact.contact_name,
                "Почта": new_contact.contact_email
            }
            with open("contacts.json", 'a', encoding='UTF-8') as f:
                json.dump(contact_dict, f, indent=2, ensure_ascii=False)
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    paginate_by = 3


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            form.add_error(None, 'Ошибка версии')
            return self.form_invalid(form)
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list')


class BlogListView(ListView):
    model = Blog
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogCreateView(CreateView):
    model = Blog
    fields = (
        'article_name',
        'contents',
        'preview',
        'create_date',
        'publication_date',
    )
    success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        if form.is_valid():
            new_art = form.save()
            new_art.slug = slugify(new_art.article_name)
            new_art.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = (
        'article_name',
        'contents',
        'preview',
        'create_date',
        'publication_date',
    )

    def get_success_url(self):
        return reverse('catalog:article', args=[self.kwargs.get('slug')])


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object()
        self.object.views_count += 1
        self.object.save()
        if self.object.views_count == 15:
            send_mail(
                subject='Поздравляем Вас!',
                message='Поздравляем! Вашу статью посмотрели уже 100 человек! Супер!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['cerbin94@gmail.com'],
                fail_silently=False
            )
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog')
