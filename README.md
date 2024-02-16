# AtomicHabits
Контекст
В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек. Заказчик прочитал книгу, впечатлился и обратился к вам с запросом реализовать трекер полезных привычек.

В рамках учебного курсового проекта реализуйте бэкенд-часть SPA веб-приложения.
### В приложении можно создавать привычку с указанием времени места выполнения, также за полезную привычку устанавливается либо награда, либо последующая приятная привычка.
### Можно создавать самостоятельную приятную привычку.
### Напоминание о привычках реализовано посредством отправки сообщений в ТелеграмБот, необходимо предоставить при регистрации пользователя
    chat_id.

### Чтобы развернуть проект необходимо выполнить следующие действия:
### Клонировать репозиторий.
### Активировать виртуальное окружение
    source env/bin/activate.bat
### Установить зависимости 
    pip3 install -r requirements.txt
### Создать файл 
    .env
### Заполнить его данными из файла
    env.sample
### Создать базу данных в PostreSQL
    atomic_habits
### Создать миграции командой
    python3 manage.py makemigrations
### И применить миграции
    python3 manage.py migrate
### Создание пользователя доступно командами:
### для суперпользователя
    python3 manage.py csu
### для обычного пользователя
    python3 manage.py create_simple_user
### Для запуска периодической рассылки в терминале набрать команды
    celery -A config worker -l info -S django
    celery -A config beat -l info -S django
### Запустить проект 
    python3 manage.py runserver
### Веб-приложение доступно по адресу
    http://127.0.0.1:8000.
    
## Документация

### Документация для API реализована посредством drf-yasg и находится на следующих эндпоинтах:
    http://127.0.0.1:8000/docs/
    http://127.0.0.1:8000/redoc/
    http://127.0.0.1:8000/swagger/
### В проекте реализовано создание трёх типов привычек:
    1) Полезная привычка с вознаграждением за выполнение
    2) Полезная привычка с последующей приятной привычкой
    3) Приятная привычка
### Модель Привычка:
    - Пользователь — создатель привычки.
    - Место — место, в котором необходимо выполнять привычку.
    - Время — время, когда необходимо выполнять привычку.
    - Действие — действие, которое представляет из себя привычка.
    - Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки.
    - Связанная привычка — привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не для приятных.
    - Периодичность (по умолчанию ежедневная) — периодичность выполнения привычки для напоминания в днях.
    - Вознаграждение — чем пользователь должен себя вознаградить после выполнения.
    - Время на выполнение — время, которое предположительно потратит пользователь на выполнение привычки.
    - Признак публичности — привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример чужие привычки.
### Полезная привычка без вознаграждения создаётся разом с приятной привычкой, также и удаляются они обе автоматически
### Пути к эндпоинтам описаны в документации, а такжк расположены в папке приложения 
    /habits_app/urls.py
### Реализована пагинация вывода не более пяти привычек на страницу
### Пользователю выводятся созданные им привычки, либо привычки других пользователей с положительным признаком публичности
### Настроены необходимые валидаторы для корректного создания/изменения привычек
### Функционал протестирован unittest
