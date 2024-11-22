# FastAPI-Movie

FastAPI-Movie — это API для управления фильмами, использующее FastAPI, PostgreSQL и внешние API для получения данных о фильмах. Приложение поддерживает операции CRUD (создание, чтение, обновление и удаление).

## Особенности

- **Взаимодействие с внешними API**: Фильмы автоматически извлекаются и сохраняются из внешних API (например, The Movie Database или других).
- **PostgreSQL**: Используется база данных PostgreSQL для хранения данных о фильмах.
- **Swagger UI**: Интерактивная документация API доступна по адресу `/docs`.
- **Асинхронная работа с API**: Для повышения производительности используются асинхронные запросы к внешним API.

## Установка

### Требования

- Python 3.9 и выше.
- Docker (для работы с контейнерами).
- PostgreSQL (для локальной работы с базой данных).

### Клонирование репозитория и создание виртуального окружения

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/LestatDamned/FastAPI-Movie.git
   cd FastAPI-Movie
   ```

2. Создайте виртуальное окружение и активируйте его:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте venv\Scripts\activate
    ```

3. Установите зависимости:
   
    ```bash
    pip install -r requirements.txt
    ```

4. Создайте файл .env в корне проекта и добавьте необходимые переменные окружения:
  
    ```bash
    DATABASE_URL=postgresql://user:password@localhost/dbname
    API_KEY=your_api_key_for_external_api
    ```

5. Постройте и запустите контейнеры:

    ```bash
    docker-compose up --build
    ```

6. Запустите приложение:

    ```bash
    uvicorn main:app --reload
    ```

  Приложение будет доступно по адресу http://localhost:8000.
  Документация API доступна по адресу http://localhost:8000/docs.

