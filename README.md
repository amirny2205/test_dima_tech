# test_dima_tech
Выполнение вот этого тестового : https://docs.google.com/document/d/1lblqae9k0wdV7q7QFjxYcC_rrDbRb5DIUHtHiKM5iz4/edit

## Запуск сервиса:

среди прочего в .env необходимо прописать следующее (открываем .env_example):

EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD - настройки для smtp

SELF_HOST, SELF_PORT - урл сервера и порт(если иной чем 80), это для воркэраунда по активации. См. "activation" в shop_main.views

PRIVATE_KEY - приватный ключ для эндпоинта payment/webhook/ . Случайная строка.

Заполнив свой .env, указывает его в docker-compose.yml ; запускаем docker-compose up

## Описание работы сервиса:

создаём пользователя POST-запросом по auth/users/ , передавая в теле username, password, email.

идём на почту, жмем ссылку. Пользователь активирован.

Идем на POST-эндпоинт localhost:8000/auth/jwt/create , передаем username, password. Получаем токен и рефреш токен

токены действуют по умолчанию час, токен можно обновить на auth/jwt/refresh/ (принимает ключ refresh)

токен можно проверить на localhost:8000/auth/jwt/verify/ , передаем ключ token

Имея токен и передавая его а authorization("Bearer /token/" или "JWT /token"), можем получить доступ к защищенным вью.

Среди них:

products/ : GET; список всех продуктов

self_info/ : GET; информация о текущем пользователе, там же его счета и транзакции

buy/ : POST; в теле ждём product_id и bill_id

есть незащищённый вью, payment/webhook/ . Ждёт POST с датой(как требуется в задании):
signature, transaction_id, user_id, bill_id, amount.
