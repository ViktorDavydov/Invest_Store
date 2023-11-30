import json

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Contacts, Category, Blog


class ProductListView(ListView):
    model = Product
    paginate_by = 3


# def index(request):
#     objects_list = Product.objects.all()
#     # context = {
#     #     'objects_list': objects_list,
#     #     'title': 'Каталог'
#     # }
#     paginator = Paginator(objects_list, 3)
#     page = request.GET.get('page')
#     try:
#         products = paginator.page(page)
#     except PageNotAnInteger:
#         products = paginator.page(1)
#     except EmptyPage:
#         products = paginator.page(paginator.num_pages)
#
#     temps = {
#         'products': products
#     }
#
#     return render(request, 'catalog/product_list.html', temps)

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


# def contacts(request):
#     all_contacts = Contacts.objects.all()
#     context = {
#         'title': 'Контакты'
#     }
#     if request.method == 'POST':
#         contact_dict = {
#             "Имя": request.POST.get('name'),
#             "Почта": request.POST.get('email'),
#             "Сообщение": request.POST.get('message')
#         }
#         with open("contacts.json", 'a', encoding='UTF-8') as f:
#             json.dump(contact_dict, f, indent=2, ensure_ascii=False)
#     return render(request, 'catalog/contacts_form.html', locals())


class ProductDetailView(DetailView):
    model = Product


# def product(request, pk):
#     chosen_product = Product.objects.get(pk=pk)
#     context = {
#         'chosen_product': chosen_product,
#     }
#     return render(request, 'catalog/product_detail.html', context)

class ProductCreateView(CreateView):
    model = Product
    fields = (
        'product_name',
        'product_description',
        'category',
        'preview',
        'price',
        'create_date',
        'final_change_date'
    )
    success_url = reverse_lazy('catalog:list')


# def add_product(request):
#     category_list = Category.objects.all()
#     context = {
#         'category_list': category_list
#     }
#     if request.method == "POST":
#         product_inf = Product(product_name=request.POST.get('name'),
#                               product_description=request.POST.get('description'),
#                               category=Category.objects.get(
#                                   category_name=request.POST.get('category')),
#                               preview=request.POST.get('preview'),
#                               price=request.POST.get('price'),
#                               create_date=request.POST.get('create_date'),
#                               final_change_date=request.POST.get('final_change_date'))
#         product_inf.save()
#     return render(request, 'catalog/product_form.html', context)

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

    # success_url = reverse_lazy('catalog:blog')

    def get_success_url(self):
        return reverse('catalog:article', args=[self.kwargs.get('pk')])


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object()
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog')
