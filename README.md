**Создание приложения Django**
1. django-admin startproject config . 
2. python manage.py startapp main
3. Настраиваем параметры запуска сервера или python manage.py runserver 
4.  Заносим в config/settings название нашего приложения 'main' в INSTALLED_APPS
5. В папке main создаем папку templates, в templates создаем папку с названием приложения 'main', в папке main создаем index.html - шаблон
6. Создаем контроллер в 'views' - просто функцию с аргументом request. Делаем return render('', 'main/index.html')
7. Создаем урл в приложение main urlpatterns = [path('', index)]
8. Находим точку входа в settings для связывания урлов - ROOT_URLCONF = 'config.urls'
9. Связываем через include - добавляем в config/urls еще один паттерн path('', include('main.urls'))


**Настройка ввода (POST)**
1. Прописываем в index.html защиту ВАЖНО! {% csrf_token %}, <form method="post"> и формы ввода
2. В контроллере прописываем логику if request.method == "POST": name = request.POST.get('name') и тд.


ORM

**Настройка подключения к БД**
1. Устанавливаем psycopg2
2. Прописываем в settings.py параметры БД: 'ENGINE': '...postgresql',
                                           'NAME': 'db_name',
                                           'USER': 'postgres',
                                           'PASSWORD': 'secret',
                                           'HOST': '127.0.0.1', - Необязательно, если сервер локальный
                                           'PORT': 5432 - Необязательно, если сервер локальный

3. В консоли подключаемся к БД: "psql -U postgres", создаем БД db_name: "create database dm_name;"

**Создание моделей и миграции**
1. Перед соданием моделей делаем миграцию "python manage.py migrate"
2. Устанавливаем Pillow (если планируем работать с медиафалами - видео, картинками, фото и тд.)
3. В models.py пишем модели (класс), наследуемся от models.Model (models импорт из django.db).
Прописываем поля в формате name = models.CharField(max_length=..., verbose_name='...') / image = models.ImageField(upload_to='directory_name/', verbose_name='...', **NULLABLE), где NULLABLE = {'blank': True, 'null': True} в самом начале.
Далее __str__, class Meta внутри нашей модели - в классе verbose_name = "название модели", verbose_name_plural = "название модели в множ. числе", ordering = ('название поля',) - упорядочивание в отображении по умолчанию (например по алфавиту и тд)
5. Создаем и выполняем миграцию "python manage.py makemigrations". В определенных случаях необходимо указывать название приложения "python manage.py makemigrations <app_name>". Далее "python manage.py migrate". В migrations можно увидеть созданный уникальный 'id' модели.
6. Далее в папке приложения создаем директорию media и в самом конце settings.py прописываем пути для сохранения медиа: MEDIA_URL = '/media/'
                                                                          MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
7. В урлах config после списка паттернов прописываем:
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
(settings - импортируем СТРОГО!!! from django.conf import settings;
static - импортируем СТРОГО!!! from django.conf.urls.static import static)

**Админка**
1. "python manage.py createsuperuser" - создаем суперпользователя (себя) - Имя, почта пароль и тд. Для отображения русского языка админки можно в settings.py сделать LANGUAGE_CODE = "ru-ru"
2. Зайти в админ панель можно добавив в конце адресной строки /admin
3. В admin.py регистрируем модель "admin.site.register(model_name)". Другой вариант:
@admin.register(model_name)
class model_nameAdmin(admin.ModelAdmin):
  list_display = ('первое_поле', 'второе поле',) - структурированное отображение, название столбцов берется из verbose_name для конкретного поля из моделей
  list_filter = ('произвольное поле',) - добавление возможности фильтрации
  search_fields = ('первое_поле', 'второе_поле',) - возможности поиска без учета регистра
В админ панеле при добавлении позиции необходимо заполнить поля, которые были прописаны при создании модели. А отображение в списке, осуществляется в виде str, прописанного в моделе.
5. 
