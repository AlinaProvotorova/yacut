# Укоротитель ссылок YaCut

YaCut умеет создавать новые ссылки для страниц которые вы предложите или использовать ваш вариант


#### Запуск приложения:
- Клонируйте репозиторий yacut командой в терминале:
```commandline
...$  git clone https://github.com/alinamalinapro/yacut.git
```
- Активируйте виртуальное окружение командой:
```commandline
...yacut$ python -m virtualenv venv && .\venv\Scripts\activate
```
- Установите библиотеки командой:
```
(venv) ...$ python3 -m pip install --upgrade pip
```

```
(venv) ...$ pip install -r requirements.txt
```
- Создайте миграции
```
(venv) ...$ flask db migrate
```


### Режимы работы:

в терминале введите команду:

```
(venv) ...$ flask run

```
Данное приложение написано с использованием фреймворка FLASK

После запуска перейдите по [ссылке](http://127.0.0.1:5000/)

Автор: [Провоторова Алина Игоревна](https://t.me/alinamalina998)