# Online shop
## Суть проекта
Небольшой интернет магазин с товарами, категориями, корзиной, оплатой и системой рекомендаций
## Установка и запуск
### Клонировать репозиторий
```
git clone https://github.com/fivan999/online_shop
```
### Конфигурация
Создайте .env файл в папке online_shop.<br>
В нем нужно указать значения:<br>
- SECRET_KEY (ваш секретный ключ, по умолчанию - default)<br>
- DEBUG (включать ли режим дебага, по умолчанию - True)<br>
- ALLOWED_HOSTS (если включен DEBUG, он ['*'], иначе по умолчанию - 127.0.0.1)<br>
- INTERNAL_IPS (для debug_toolbar, по умолчанию - 127.0.0.1) <br>
- REDIS_HOST (хост базы данных redis, по умолчанию - localhost)
- REDIS_DB=0 (номер базы данных redis, по умолчанию - 0)
- CELERY_TASK_ALWAYS_EAGER (выполнять ли задания от celery синхронно, запуск rabbitmq и celery не требуется при true, по умолчанию - true)
- RABBITMQ_USER (имя пользователя rabbitmq)
- RABBITMQ_PASS (пароль пользователя rabbitmq)
- RABBITMQ_HOST (хост rabbitmq)
#### Настройка отправки почты
Если вы хотите, чтобы письма только сохранялись в папке sent_emails, в .env файле укажите USE_SMTP=false<br>
Иначе нужно указать несколько значений:
- USE_SMTP=True
- EMAIL_HOST (смтп, которое вы используете)
- EMAIL_PORT (порт нужного смтп)
- EMAIL_USE_TLS (true или false, по умолчанию - true), EMAIL_USE_SSL (true или false, по умолчанию - false). True должно быть только одно из двух значений
- EMAIL_HOST_USER (почта)
- EMAIL_HOST_PASSWORD (пароль от почты)
#### Настройки платежной системы Stripe
- STRIPE_PUBLISHABLE_KEY (публичный ключ stripe)
- STRIPE_SECRET_KEY (секретный ключ stripe)
- STRIPE_WEBHOOK_SECRET (секретный ключ от вебхука в stipe, чтобы при оплате заказа stripe дергал вебхук, который помечает заказ как оплаченный после оплаты)
Пример .env файла - .env.example
### Запуск
Скачайте Docker: https://www.docker.com/<br>
Запустите Docker<br>
В терминале:
```
docker-compose --env-file online_shop/.env up 
```
Сервер запустится по адресу http://localhost:8000/
## Использованные технологии
- Асинхронная отправка почты с помощью Celery и брокера RabbitMQ
- Redis для работы системы рекомендаций на основе подсчета количества товаров, купленных вместе друг с другом
- Корзина товаров, реализованная на сессиях
- Интеграция с платежной системой Stripe
- Система купонов (скидок)
- Сайт доступен на английском и русском языках