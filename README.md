# praktikum_new_diplom
# «Продуктовый помощник»

---
## Локальная версия:
- #### Зарегистрироваться.
- #### создавать рецепты.
- #### подписывать на авторов
- #### Скачивать рецепты
---

### Настройки докера после ревьюлакальной версии:


## Работа API

#### 1. Создается пользователь:

POST : https://foodisgood.ddns.net/api/users/

```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}

respone 200 : 

{
"email": "vpupkin@yandex.ru",
"id": 0,
"username": "vasya.pupkin",
"first_name": "Вася",
"last_name": "Пупкин"
}

```

#### 2. Токен. 

POST : https://foodisgood.ddns.net/api/auth/token/login/

```
{
  "password": "string",
  "email": "string"
}

respone 201 : 

{
  "auth_token": "здесть_будет_указа_токен"
}

```
#### 3. Рецепт. С использование токена. 


POST : https://foodisgood.ddns.net/api/recipes/

```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}

response 200 :

{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}

```

#### Документация по запросам "http://localhost/api/docs/redoc.html"