![Python](https://img.shields.io/badge/Python-3.12-green?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-green?logo=Django)
![Django-REST](https://img.shields.io/badge/Django_rest_framework-green?logo=Django)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-green?logo=FastAPI)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-pink?logo=SQLAlchemy)
![PostgreSQL](https://img.shields.io/badge/Postgres-16-darkblue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-blue?logo=docker)
![Docker-Compose](https://img.shields.io/badge/DockerCompose-blue?logo=docker)

---

Этот репозиторий содержит два одтельных приложения одно на django, django-rest-framework и другое на fastapi

Django Task Manager - это веб-приложение для управления задачами, разработанное на Django и Django REST Framework. Приложение предоставляет полный цикл CRUD (Create, Read, Update, Delete) операций для управления задачами с системой аутентификации пользователей.
FastAPI Task Manager - это это высокопроизводительный микросервис для управления задачами, построенный на современном асинхронном фреймворке FastAPI. Сервис предоставляет полный цикл CRUD (Create, Read, Update, Delete) управления задачами.

#### Пометка
По поводу тестирования приложения на django сразу хотел сказать, что видел, какие фреймворки указаны в тестовом задании, но всё равно решил, что целесообразнее использовать встроенное джанговское тестирование. Объясню почему: я не вижу смысла использовать тут pytest или другие фреймворки для тестирования — это нужно заморачиваться с конфигами, импортами всего settings и так далее. В Django уже всё готово для тестирования, просто пиши.
Тестирование на fastapi приложении реализованно на pytest.

## Django
Docs
|AUTHORIZE | GET | GET_LIST |
|----------|-----|----------|
| <img width="1845" height="911" alt="изображение" src="https://github.com/user-attachments/assets/3598d980-727d-47f0-82ed-5996f84bc049" /> | <img width="908" height="728" alt="изображение" src="https://github.com/user-attachments/assets/924157f2-93b9-4a6f-99f4-11716d92dca4" /> | <img width="935" height="719" alt="изображение" src="https://github.com/user-attachments/assets/f06495e1-33e8-4d7d-a427-cdffe6cf2c3f" /> |


|CREATE | UPDATE | DELETE |
|-------|--------|--------|
| <img width="934" height="911" alt="изображение" src="https://github.com/user-attachments/assets/35fbf822-5195-4b3f-8d0b-bfa7b59e8d9a" /> | <img width="1215" height="901" alt="изображение" src="https://github.com/user-attachments/assets/2f9e3732-62fa-44bf-a45b-975d6e2ea004" />  <img width="1411" height="903" alt="изображение" src="https://github.com/user-attachments/assets/c516161e-fa97-496c-89b0-b6d4eb3f1196" />  | <img width="945" height="719" alt="изображение" src="https://github.com/user-attachments/assets/63c364a0-4b0b-4036-a864-a1522f4d0ec2" /> |

## FastAPI
Docs
| GET | GET_LIST |
|-----|----------|
| <img width="1527" height="769" alt="Снимок экрана 2025-08-31 210332" src="https://github.com/user-attachments/assets/89e3bbc3-c584-439e-86b1-7cb31deede6b" /> <img width="1473" height="344" alt="Снимок экрана 2025-08-31 210349" src="https://github.com/user-attachments/assets/65d25bd8-c6f6-4854-a9fa-75fd1a3af8d2" /> | <img width="1484" height="869" alt="Снимок экрана 2025-08-31 210211" src="https://github.com/user-attachments/assets/cdd3f509-171e-4ee4-bb53-953ba136e73a" /> <img width="1524" height="507" alt="Снимок экрана 2025-08-31 210218" src="https://github.com/user-attachments/assets/d1518637-1323-405e-85af-9f52830e0ff4" /> |


|CREATE | UPDATE | DELETE |
|-------|--------|--------|
| <img width="1456" height="864" alt="Снимок экрана 2025-08-31 210503" src="https://github.com/user-attachments/assets/36fb153c-3342-41b9-ad6a-26351a1fc05f" /> <img width="1475" height="345" alt="Снимок экрана 2025-08-31 210509" src="https://github.com/user-attachments/assets/4977d48f-4c21-42eb-b0a5-845ecc1f8592" /> | <img width="1467" height="630" alt="Снимок экрана 2025-08-31 210546" src="https://github.com/user-attachments/assets/e83e791c-9df4-49db-9983-43df5bda242b" /> <img width="1473" height="730" alt="Снимок экрана 2025-08-31 210553" src="https://github.com/user-attachments/assets/5ad81dde-0275-4d42-95ee-a7faa93a9f1e" /> | <img width="1503" height="877" alt="Снимок экрана 2025-08-31 210628" src="https://github.com/user-attachments/assets/91cfba02-0b3d-444c-9023-11296995f63f" /> |

## Project Structure

```shell
.github/
├── workflows/
    ├── ci-backend.yaml                 # A CI file for the backend app that consists of `build`, `test`
django_task_manager/
├── core
├── tasks
├── Docker
├── .pylintrc
fastapi_task_manager/
├── app/
    ├── api/
        ├── dependencies/               # Dependency injections
            ├── session.py
            ├──repository.py
        ├── routes/                     # Endpoints
            ├── tasks.py                # task routes
        ├── endpoints.py                # Endpoint task(crud)
    ├── config/
        ├── settings/
            ├── base.py                 # Base settings / settings parent class
                ├── development.py      # Development settings (prod, test in feature)
                ├── environments.py     # Enum with PROD, DEV, STAGE environment
        ├── events.py                   # Registration of global events
        ├── manager.py                  # Manage get settings
    ├── models/
        ├── db/
            ├── task.py                 # task class for database entity
        ├── schemas/
            ├── account.py              # Account classes for data validation objects
            ├── base.py                 # Base class for data validation objects
    ├── repository/
        ├── crud/
            ├── task.py                 # C. R. U. D. operations for Task entity
            ├── base.py                 # Base class for C. R. U. D. operations
        ├── database.py                 # Database class with engine and session
        ├── events.py                   # Database events
        ├── table.py                    # Custom SQLAlchemy Base class
    ├── utils/
        ├── exceptions/
            ├── database.py             # Custom `Exception` class
        ├── formatters/
            ├── datetime_formatter.py   # Reformat datetime into the ISO form
            ├── field_formatter.py      # Reformat snake_case to camelCase
    ├── main.py                         # Our main backend server app
├── tests/
    ├── api/                            # Integration API tests
    ├── unit_tests/                     # Unit tests
        ├── test_model.py               # Testing model
        ├── test_repo.py                # Testing repo (crud) 
        ├── test_schemas.py             # Testing schemas
    ├── conftest.py                     # The fixture codes and other base test codes
├── Dockerfile                          # Docker configuration file for backend application
├── .pylintrc
README.md                               # Documentation for backend app
requirements.txt                        # Packages installed for backend app
.dockerignore                           # A file that list files to be excluded in Docker container
.gitignore                              # A file that list files to be excluded in GitHub repository
.pre-commit-config.yaml                 # A file with Python linter hooks to ensure conventional commit when committing
README.md                               # The main documentation file for this template repository
docker-compose.yaml                     # The main configuration file for setting up a multi-container Docker
```

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
