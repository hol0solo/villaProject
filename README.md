# Villa Project

Проект по продаже вилл, созданный с использованием Django. Включает интеграцию Stripe для оплаты, кастомное логирование через соцсети и асинхронную обработку задач с Celery.

## Стек технологий

- Python 3+
- Django 4.2
- Celery + Redis
- PostgreSQL
- OAuth v2.0, WebHook
- Django REST Framework (DRF)
- Stripe
- SQLAlchemy

## Установка и запуск

1. Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/hol0solo/villaProject.git
cd villaProject
```

2. Создайте виртуальное окружение и активируйте его:

```bash
python3.9 -m venv venv
source venv/bin/activate
```

3. Установите зависимости:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Настройте файл `.env` с такими переменными:

```plaintext
SECRET_KEY=ваш_секретный_ключ
STRIPE_SECRET_KEY=ваш_stripe_ключ
DATABASE_URL=ваш_postgresql_url
REDIS_URL=ваш_redis_url
```

5. Выполните миграции и загрузите фикстуры:

```bash
python manage.py migrate
python manage.py loaddata villaProject/villa/fixtures/data.json
python manage.py runserver
```

6. Запустите Redis и Celery:

```bash
redis-server
celery -A villa worker --loglevel=INFO
```

## Структура проекта

- `media/` — место для сбора фото и видео
- `mixins/` — миксин, добавляющий название страницы
- `orders/` — логика заказов + подключенный Stripe
- `static/` — статичные файлы для отображения страниц
- `templates/socialaccount/` — шаблоны для кастомного логирования
- `users/` — логика работы с пользователями
- `villa/` — основное приложение

## Лицензия

Проект распространяется под лицензией MIT.

