# Монитор финансовых рынков

Веб-приложение для мониторинга финансовых рынков с REST API.

## Технологии

- Backend: Django + Django REST Framework
- Database: PostgreSQL
- Authentication: JWT (SimpleJWT)
- Docker & Docker Compose

## Требования

- Python 3.11+
- PostgreSQL 15+ (или Docker)

## Запуск проекта

### Вариант 1: С использованием Docker (рекомендуется)

```bash
cd backend

# Сборка и запуск контейнеров
docker-compose up --build

# Приложение доступно по адресу http://localhost:8000
```

### Вариант 2: Локальный запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте переменные окружения (опционально):
```bash
export POSTGRES_DB=financial_markets
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

3. Примените миграции:
```bash
python manage.py migrate
```

4. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

5. Запустите сервер:
```bash
python manage.py runserver 0.0.0.0:8000
```

## API Endpoints

### Аутентификация
- `POST /api/auth/register/` - Регистрация пользователя
- `POST /api/auth/login/` - Вход (получение JWT токенов)
- `POST /api/auth/token/refresh/` - Обновление access токена

### Активы
- `GET /api/assets/` - Список активов (параметры: search, type)
- `GET /api/assets/{id}/` - Детали актива
- `GET /api/assets/{id}/prices/` - Котировки актива
- `POST /api/assets/` - Создание актива (только admin)

### Новости
- `GET /api/news/` - Список новостей (параметр: asset_id)

### Списки наблюдения (требуется авторизация)
- `GET /api/watchlists/` - Список watchlist пользователя
- `POST /api/watchlists/` - Создание watchlist
- `POST /api/watchlists/{id}/add/` - Добавить актив в watchlist
- `DELETE /api/watchlists/{id}/remove/` - Удалить актив из watchlist

### Админ панель
- `/admin/` - Django админ панель

## Формат запросов

### Регистрация
```json
{
  "email": "user@mail.com",
  "password": "password123"
}
```

### Вход
```json
{
  "email": "user@mail.com",
  "password": "password123"
}
```

Ответ:
```json
{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "user": {
    "id": 1,
    "email": "user@mail.com"
  }
}
```

### Авторизация в запросах
Добавьте заголовок:
```
Authorization: Bearer <access_token>
```

## Структура проекта

```
backend/
 ├── config/          # Настройки Django
 ├── users/           # Пользователи и аутентификация
 ├── assets/          # Активы и котировки
 ├── watchlists/      # Списки наблюдения
 ├── news/            # Новости
 ├── manage.py        # Управление проектом
 ├── requirements.txt # Зависимости
 ├── Dockerfile       # Docker образ
 └── docker-compose.yml # Docker Compose конфигурация
```

## Модели данных

- **User** - Пользователь (email, password, is_admin, created_at)
- **Asset** - Актив (ticker, name, type, sector, created_at)
- **PriceData** - Котировки (asset_id, open, close, high, low, volume, timestamp)
- **MarketNews** - Новости (title, content, source, published_at, asset_id)
- **Watchlist** - Список наблюдения (user_id, name, created_at)
- **WatchlistAsset** - Связь многие-ко-многим (watchlist_id, asset_id)
