#Instal dependencies

```
pip install -r requirements.txt

```

#Запуск

При первичном запуске произвести миграции

```
./manage.py migrate
```

При первичном запуске заполнить модель начальными данными

```
./manage.py loaddata rsqm\rsqm_fixture.json
```

При первичном запуске следует создать суперпользователя

```
./manage.py createsuperuser
```

Добавить файл с локальными настройками
```
cp rsqm/settings/local.py.example rsqm/settings/local.py
```

Сам запуск

```
./manage.py runserver
```