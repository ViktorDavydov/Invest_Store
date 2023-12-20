import json

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, \
    PermissionRequiredMixin
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm, VersionBaseInLineFormSet, BlogForm, \
    ModeratorForm
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

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')
    permission_required = 'catalog.change_product'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1,
                                               formset=VersionBaseInLineFormSet)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if form.is_valid():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                return self.form_invalid(form)
        return super().form_valid(form)

    def get_form_class(self):
        if self.request.user.is_staff and self.request.user.groups.filter(
                name='moderator').exists():
            return ModeratorForm
        return ProductForm

    def test_func(self):
        _user = self.request.user
        _instance: Product = self.get_object()
        custom_perms: tuple = (
            'catalog_app.set_is_published',
            'catalog_app.set_category',
            'catalog_app.set_product_description',
        )
        if _user.is_superuser or _user == _instance.owner:
            return True
        elif _user.groups.filter(name='moderator') and _user.has_perms(custom_perms):
            return True
        return self.handle_no_permission()


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list')


class BlogListView(ListView):
    model = Blog
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        if form.is_valid():
            new_art = form.save()
            new_art.slug = slugify(new_art.article_name)
            new_art.save()
        return super().form_valid(form)

    def test_func(self):
        _user = self.request.user
        _instance: Blog = self.get_object()
        if _user.is_superuser or _user.groups.filter(name='content_manager'):
            return True
        return self.handle_no_permission()


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm

    def get_success_url(self):
        return reverse('catalog:article', args=[self.kwargs.get('slug')])

    def test_func(self):
        _user = self.request.user
        _instance: Blog = self.get_object()
        if _user.is_superuser or _user.groups.filter(name='content_manager'):
            return True
        return self.handle_no_permission()


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object()
        self.object.views_count += 1
        self.object.save()
        if self.object.views_count == 20:
            send_mail(
                subject='Поздравляем Вас!',
                message='Поздравляем! Вашу статью посмотрели уже 100 человек! Супер!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['cerbin94@gmail.com'],
                fail_silently=False
            )
        return self.object


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('catalog:blog')
