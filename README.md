Создание приложения Django
1. django-admin startproject config . 
2. python manage.py startapp main
3. Настраиваем параметры запуска сервера или python manage.py runserver 
4.  Заносим в config/settings название нашего приложения 'main' в INSTALLED_APPS
5. В папке main создаем папку templates, в templates создаем папку с названием приложения 'main', в папке main создаем index.html - шаблон
6. Создаем контроллер в 'views' - просто функцию с аргументом request. Делаем return render('', 'main/index.html')
7. Создаем урл в приложение main urlpatterns = [path('', index)]
8. Находим точку входа в settings для связывания урлов - ROOT_URLCONF = 'config.urls'
9. Связываем через include - добавляем в config/urls еще один паттерн path('', include('main.urls'))


Настройка ввода (POST)
1. Прописываем в index.html защиту ВАЖНО! {% csrf_token %}, <form method="post"> и формы ввода
2. В контроллере прописываем логику if request.method == "POST": name = request.POST.get('name') и тд.