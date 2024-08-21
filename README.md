<h1 align='center'>Новостной сайт</h1>

Проект представляет собой новостной сайт сделанный с использованием технологии Django. В проекте реализована авторизация, добавления комментариев, изменение профиля, регистрация с активацией через почту, просмотр новостей. В проекте использовались Celery, Redis, Pillow, PostgreSQL


### Endpoint

#### Authentication

* **/auth/users/** (Регистрация пользователя)
* **/auth/token/login/** (Авторизация пользователя)
* **/api/users/logout/** (Выход пользователя)


#### Users

* **/magazine_api/user/** (Вывод всех пользователей, 'GET')
* **/magazine_api/user/** (Добавление пользователя, 'POST')
* **/magazine_api/user/pk/** (Чтение пользователя, 'GET')
* **/magazine_api/user/pk/** (Редактирование пользователя, 'PUT')
* **/magazine_api/user/pk/** (Удаление пользователя, 'DELETE')
* **/magazine_api/user/del_product/?id=&name** (Удаление из корзины, 'GET')
* **/magazine_api/user/add_to_cart/?id=&q** (Добавление в корзину, 'GET')
* **/magazine_api/user/get_orders/?id=&q** (Получение заказов, 'GET')
  

#### Product

* **/magazine_api/product/** (Вывод всех продуктов, 'GET')
* **/magazine_api/product/** (Добавление продукта, 'POST')
* **/magazine_api/product/pk/** (Чтение продукта, 'GET')
* **/magazine_api/product/pk/** (Редактирование продукта, 'PUT')
* **/magazine_api/product/pk/** (Удаление продукта, 'DELETE')
* **/magazine_api/product/products_search/?q** (Поиск продукта, 'GET')
* **/magazine_api/product/search_by_category/?category** (Фильтрация продуктов по категории, 'GET')
* **/magazine_api/product/get_all_reviews/?id** (Получение всех отзывов, 'GET')


#### Category

* **/magazine_api/category/** (Вывод всех категорий товаров, 'GET')
* **/magazine_api/category/** (Добавление категории, 'POST')
* **/magazine_api/category/pk/** (Чтение категории, 'GET')
* **/magazine_api/category/pk/** (Редактирование категории, 'PUT')
* **/magazine_api/category/pk/** (Удаление категории, 'DELETE')


#### Order

* **/magazine_api/order/** (Вывод всех заказов, 'GET')
* **/magazine_api/order/** (Добавление заказа, 'POST')
* **/magazine_api/order/pk/** (Чтение заказа, 'GET')
* **/magazine_api/order/pk/** (Редактирование заказа, 'PUT')
* **/magazine_api/order/pk/** (Удаление заказа, 'DELETE')


#### Review

* **/magazine_api/review/** (Вывод всех категорий отзывов, 'GET')
* **/magazine_api/review/** (Добавление отзыва, 'POST')
* **/magazine_api/review/pk/** (Чтение отзыва, 'GET')
* **/magazine_api/review/pk/** (Редактирование отзыва, 'PUT')
* **/magazine_api/review/pk/** (Удаление отзыва, 'DELETE')

### Install 

    pip install -r requirements/prod.txt

### Usage

    python manage.py test --settings=navos.settings.prod

### License

  Этот проект лицензирован под MIT License.
