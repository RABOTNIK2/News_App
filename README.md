<h1 align='center'>Новостной сайт</h1>

Проект представляет собой новостной сайт сделанный с использованием технологии Django. В проекте реализована авторизация, добавления комментариев, изменение профиля, регистрация с активацией через почту, просмотр новостей. В проекте использовались Celery, Redis, Pillow, PostgreSQL


### Endpoint

#### Authentication, Registration

* **/news/login/** (Авторизация пользователя)
* **/news/account_sent/** (Отправка email для активации аккаунта)
* **/news/account_complete/** (Успешная активация)
* **/news/register/** (Регистрация пользователя)


#### Profile

* **/news/profile/<pk>/** (Профиль пользователя)
* **/news/profile/logout/** (Выход из аккаунта)
* **/news/profile/update/<pk>/** (Изменение личных данных)
* **/news/profile/password_change/<pk>/** (Изменение пароля)
* **/news/user/pk/** (Удаление пользователя, 'DELETE')
* **/news/profile/image/<pk>/** (Изменение фото профиля)
  

#### News, Comments

* **/news/main/** (Вывод всех новостей)
* **/news/main/<pk>/** (Просмотр конкретной новости, 'GET')
* **/news/main/<pk>/** (Добавление комментария, 'POST')
* **/news/main/<pk>/<comment>/** (Изменение комментария)
* **/news/main/<pk>/<del_comment>/** (Удаление комментария)


### Usage

    docker-compose up --build

### License

  Этот проект лицензирован под MIT License.
