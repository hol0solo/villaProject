# Проект: Сайт по продаже вилл

## Описание
Проект представляет собой веб-приложение для продажи вилл, разработанное с использованием Django. Сайт позволяет пользователям просматривать, фильтровать и искать доступные виллы, а также взаимодействовать с системой через личные кабинеты.

## Функционал
- Регистрация и авторизация пользователей
- Просмотр каталога вилл с фильтрами
- Детальная страница каждой виллы
- Управление объявлениями (CRUD)
- Логирование через социальные сети (OAuth v2.0)
- Прием платежей через Stripe

## Стек технологий
- **Backend:** Python 3+, Django 4.2
- **БД:** PostgreSQL
- **Асинхронные задачи:** Celery + Redis
- **API:** Django REST Framework, WebHook
- **Аутентификация:** OAuth v2.0
- **Платежная система:** Stripe
- **Логирование:** Кастомная настройка логов

## Установка и запуск
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/hol0solo/villaProject.git
   cd villaProject
   ```
2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Настройте переменные окружения, создав файл `.env` и добавив в него:
   ```
   DATABASE_URL=URL вашей базы данных PostgreSQL
   STRIPE_SECRET_KEY=Ваш секретный ключ Stripe
   OAUTH_CLIENT_ID=Ваш клиент ID OAuth
   OAUTH_CLIENT_SECRET=Ваш клиент Secret OAuth
   ```
5. Выполните миграции и запустите сервер:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
6. Запустите Celery и Redis:
   ```bash
   redis-server
   celery -A villaProject worker --loglevel=INFO
   ```

## Структура проекта
- `core/` — основная логика приложения
- `villas/` — приложение для управления виллами
- `users/` — аутентификация и управление пользователями
- `payments/` — обработка платежей через Stripe

## Контакты
Автор: [hol0solo](https://github.com/hol0solo)

## Лицензия
Этот проект распространяется под лицензией MIT.

