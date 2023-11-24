---19.2---

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


---20.1---

ORM

**Настройка подключения к БД**
1. Устанавливаем psycopg2
2. Прописываем в settings.py параметры БД: 'ENGINE': '...postgresql',
                                           'NAME': 'db_name',
                                           'USER': 'postgres',
                                           'PASSWORD': 'secret',
                                           'HOST': '127.0.0.1', - Необязательно, если сервер локальный
                                           'PORT': 5432 - Необязательно, если сервер локальный

3. В консоли подключаемся к БД: "psql -U postgres", создаем БД db_name: "create database <dm_name>;"

**Создание моделей и миграции**
1. Перед соданием моделей делаем миграцию "python manage.py migrate"
2. Устанавливаем Pillow (если планируем работать с медиафалами - видео, картинками, фото и тд.)
3. В models.py пишем модели (класс), наследуемся от models.Model (models импорт из django.db).
Прописываем поля в формате name = models.CharField(max_length=..., verbose_name='...') / image = models.ImageField(upload_to='<directory_name>/', verbose_name='...', **NULLABLE), где NULLABLE = {'blank': True, 'null': True} в самом начале.
Далее __str__, class Meta внутри нашей модели - в классе verbose_name = "название модели", verbose_name_plural = "название модели в множ. числе", ordering = ('<название поля>',) - упорядочивание в отображении по умолчанию (например по алфавиту и тд)
5. Создаем и выполняем миграцию "python manage.py makemigrations". В определенных случаях необходимо указывать название приложения "python manage.py makemigrations <app_name>". Далее "python manage.py migrate". В migrations можно увидеть созданный уникальный 'id' модели.
6. Далее в папке приложения создаем директорию media и в самом конце settings.py прописываем пути для сохранения медиа: MEDIA_URL = '/media/' и MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
8. В урлах config после списка паттернов прописываем:
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
(settings - импортируем СТРОГО!!! from django.conf import settings;
static - импортируем СТРОГО!!! from django.conf.urls.static import static)

**Админка**
1. "python manage.py createsuperuser" - создаем суперпользователя (себя) - Имя, почта пароль и тд. Для отображения русского языка админки можно в settings.py сделать LANGUAGE_CODE = "ru-ru"
2. Зайти в админ панель можно добавив в конце адресной строки /admin
3. В admin.py регистрируем модель "admin.site.register(<model_name>)". Другой вариант:
@admin.register(<Model_name>)
class <Model_name>Admin(admin.ModelAdmin):
  list_display = ('<первое_поле>', '<второе поле>',) - структурированное отображение, название столбцов берется из verbose_name для конкретного поля из моделей
  list_filter = ('<произвольное поле>',) - добавление возможности фильтрации
  search_fields = ('<первое_поле>', '<второе_поле>',) - возможности поиска без учета регистра
В админ панеле при добавлении позиции необходимо заполнить поля, которые были прописаны при создании модели. А структурированное отображение в списке, осуществляется в виде str, прописанного в моделях.

**Наполнение БД**
Shell
1. Для удобства отображения можем установить ipython
2. Запускаем инструмент "python manage.py shell"
3. В консоли shell для работы с моделью загружаем её "from <app_name>.models import <model_name>"
4. Работа с данными выстроена так: <Model_name>.objects.all(), где objects менеджер моделей для использования методов all, filter, get и тд. Другие варианты получения инф из базы данных: <model_name>.objects.get(pk=1) (в конце можно добавить ._ _dict_ _ для удобства отображения), <Model_name>.objects.filter(<название_поля> = <значение поля>), <Model_name>.objects.exclude(<название_поля> = <значение поля>) - исключение, и т.д. При указании нескольких условий фильтрации или исключения, всегда под капотом используется оператор AND

Фикстуры
1. dumpdata - сохранение данных из текущей БД. "python manage.py dumpdata > data.json". ВАЖНО - следить за кодировкой, бывает сохраняется коряво кириллица. Когда приложений много необходимо указать наименование "python manage.py dumpdata <app_name> > data.json"
2. loaddata - загрузка данных в текущую БД. Все тоже самое - "python manage.py loaddata <app_name> data.json"
Если, например, pk не уникальный - будет добавляться новая запись в БД каждый раз при loaddata

**Кастомные команды**
1. Создаем ПАКЕТ management в папке приложения
2. В management создаем ПАКЕТ commands
3. В commands создаем файл .py с нзванием, по которому будем вызывать команду в формате:
from django.core.management import BaseCommand - базовый обязательный класс

class Command(BaseCommand):
  def handle(self, *args, **options):
    print('Hi, Sky!')

**Наполнение БД**
1. Используем class Command(BaseCommand):
2. def handle(self, *args, **options): тут прописываем исходный список словарей (<model_name>_list = [{},{},{}]) с ключами - названия полей, значениями - что ходим добавить.
3. Создаем пустой список для заполнения <model_name>_for_create = [] и прописываем цикл for <model_name>_item in <model_name>_list:
4. В цикле пишем <model_name>_for_create.append(<Model_name>(**<model_name>_item))
5. Вне цикла пишем <Model_name>.objects.bulk_create(<model_name>_for_create)



