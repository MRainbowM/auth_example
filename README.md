# auth_example

## Запуск проекта

##### Создание дефолтных переменных окружения

```shell
cp .env.example .env
```

##### Сборка и запуск докера

```shell
docker compose -f docker-compose.yml up --build
```

##### Запуск бэкенда

```shell
docker-compose exec backend python -m uvicorn config.asgi:application --reload --host 0.0.0.0 --port 8006
```

##### Создание тестовых данных

```shell
docker compose exec backend python manage.py create_test_data
```

## Миграции

##### Создание миграций

```shell
docker-compose exec backend python manage.py makemigrations
```

##### Применение миграций

```shell
docker-compose exec backend python manage.py migrate
```

##### Создание суперпользователя

```shell
docker-compose -f docker-compose.yml exec backend python manage.py createsuperuser
```

## Разработка

### Mutagen

##### Запуск синхронизации файлов докера и локальной машины

```shell
mutagen project start
```

##### Остановить  Mutagen

```shell
mutagen project terminate
```

##### Посмотреть статус проекта

```shell
mutagen project list
```

##### Посмотреть расширенный вывод

```shell
mutagen sync list --long
```

## Тесты

##### Запуск тестов

```shell
docker compose exec backend pytest
```

## Ссылки

##### Сваггер

```
http://localhost:8080/api/docs#/
```

##### Админка Django

```
http://localhost:8080/admin/
```

