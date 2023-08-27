# Foodgram - gродуктовый помощник
Прроект предназначен для публикации рецептов различных блюд.
Здесь можно делиться своими любимыми рецептами, добавлять в избранное рецепты других пользователей, формировать список покупок, необходимый для выбранных рецептов.

---
## Технологии:
- #### Django.
- #### Python.
- #### Docker
---

## Запуск проекта
- #### Клонировать репозиторий
git clone https://github.com/pavelmakhnin/foodgram-project-react

- #### Собрать образы
cd frontend 
docker build -t username/foodgram_frontend: latest .
cd ../backend  
docker build -t username/foodgram_backend: latest .
cd ../infra  
docker build -t username/foodgram_gateway: latest .

- #### Собрать контейнеры
Из директории infra выполнить команду: docker compose -f docker-compose.production.yml up –-build

- #### Применить миграции
Из директории infra выполнить команду: docker compose -f docker-compose.production.yml manage.py migrate

- #### Создать superuser
Из директории infra выполнить команду: docker compose -f docker-compose.production.yml createsuperuser

- #### Собрать статику
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend cp -r /app/static/. /static/

- #### Загрузить ингредиенты
docker compose -f docker-compose.production.yml exec backend python manage.py load_ingredients_csv

## Подготовка и деплой на сервере

#### Создаём на сервере новую директорию и сразу в неё переходим.
- sudo mkdir foodgram && cd foodgram

#### Создаём в директории foodgram файл .env
ALLOWED_HOSTS=yourhost,158.160.xxx.xxx,127.0.0.1,localhost,backend
SECRET_KEY=yoursecretkey
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432
DEBAG=FALSE

#### Cоздаём файл докер-компос.
- sudo touch docker-compose.production.yml 

#### Переносим в файл докер-компосе на сервере содержимое локального файла.
- sudo nano docker-compose.production.yml 
Копируем cntrl+shift+c и переносим cntrl+shift+v

#### Применить миграции
- sudo docker compose -f docker-compose.production.yml manage.py migrate

#### Создать superuser
- sudo docker compose -f docker-compose.production.yml createsuperuser

#### Собрать статику
- sudo docker-compose exec backend python manage.py collectstatic 
- sudo docker-compose exec backend cp -r /app/static/. /static/

#### Загрузить ингредиенты
- sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_ingredients_csv


## Данные для входа в админку:
Логин: pasha1904@yandex.ru
Пароль: Test2023

## Проект доступен по адресу
http://158.160.11.193/

