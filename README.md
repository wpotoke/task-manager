![Python](https://img.shields.io/badge/Python-3.12-green?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-green?logo=Django)
![Django-REST](https://img.shields.io/badge/Django_rest_framework-green?logo=Django)
![PostgreSQL](https://img.shields.io/badge/Postgres-16-darkblue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-blue?logo=docker)
![Docker-Compose](https://img.shields.io/badge/DockerCompose-blue?logo=docker)

---

Django Task Manager - это веб-приложение для управления задачами, разработанное на Django и Django REST Framework. Приложение предоставляет полный цикл CRUD (Create, Read, Update, Delete) операций для управления задачами с системой аутентификации пользователей.

#### Пометка
По поводу тестирования сразу хотел сказать, что видел, какие фреймворки указаны в тестовом задании, но всё равно решил, что целесообразнее использовать встроенное джанговское тестирование. Объясню почему: я не вижу смысла использовать тут pytest или другие фреймворки для тестирования — это нужно заморачиваться с конфигами, импортами всего settings и так далее. В Django уже всё готово для тестирования, просто пиши.
Я пока не знаю, в какой форме, но хочу сделать это тестовое и на Django, и на FastAPI. И на FastAPI как раз использую pytest или посмотрю, что за Gauge.


Docs
|AUTHORIZE | GET | GET_LIST |
|----------|-----|----------|
| <img width="1845" height="911" alt="изображение" src="https://github.com/user-attachments/assets/3598d980-727d-47f0-82ed-5996f84bc049" /> | <img width="908" height="728" alt="изображение" src="https://github.com/user-attachments/assets/924157f2-93b9-4a6f-99f4-11716d92dca4" /> | <img width="935" height="719" alt="изображение" src="https://github.com/user-attachments/assets/f06495e1-33e8-4d7d-a427-cdffe6cf2c3f" /> |


|CREATE | UPDATE | DELETE |
|-------|--------|--------|
| <img width="934" height="911" alt="изображение" src="https://github.com/user-attachments/assets/35fbf822-5195-4b3f-8d0b-bfa7b59e8d9a" /> | <img width="1215" height="901" alt="изображение" src="https://github.com/user-attachments/assets/2f9e3732-62fa-44bf-a45b-975d6e2ea004" />  <img width="1411" height="903" alt="изображение" src="https://github.com/user-attachments/assets/c516161e-fa97-496c-89b0-b6d4eb3f1196" />  | <img width="945" height="719" alt="изображение" src="https://github.com/user-attachments/assets/63c364a0-4b0b-4036-a864-a1522f4d0ec2" /> |


#### Установка
**Клонируйте репозиторий:**

```bash
git clone https://github.com/wpotoke/task_manager.git
cd task_manager
````
**Активируйте виртуальное окружени и установите зависисмости:**
```
python -m venv venv
pip install -r requirements.txt
```
**Создайте файл переменных окружения:**
.env
```
SECRET_KEY = secret key

# database
ENGINE = "django.db.backends.postgresql"
NAME = "NAME_DB"
USER = "USERNAME"
PASSWORD = "PASS"
HOST = "db"
PORT = "5432"

```
**Сгенерируйте SECRET_KEY (если необходимо) и вставьте его в файл .env:**

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
**Создайте пользователя и базу данных, также передайте права на пользование и укажите кодировку**
(pqsl)
```pqsl
CREATE USER your_username WITH PASSWORD 'your_password';
CREATE DATABASE your_databasename OWNER your_username ENCODING 'UTF8' LC_COLLATE 'ru_RU.UTF8' LC_CTYPE 'ru_RU.UTF8' TEMPLATE=template0;
```
**Соберите и запустите контейнеры:**
```bash
docker-compose up --build
```
**Примените миграции**
```
cd django_task_manager
docker-compose exec web python manage.py migrate
```
**Создайте админа**
```
docker-compose exec web python manage.py createsuperuser
Username (leave blank to use 'task_manager'): root
Email address: enter
Password: root
Password (again): root
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```
**Потыкать проверить работу**

Переходите по адресу 127.0.0.1:8000/api/v1/docs/

### Тестирование
```
docker-compose exec web python manage.py test
```
