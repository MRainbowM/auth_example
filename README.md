# auth_example



## Описание системы разграничения прав доступа


#### Основные таблицы для реализации разграничения прав:
- Role (apps.authorization)
- RolePermission (apps.authorization)
- UserRole (apps.authorization)

#### Role
Таблица, хранящая список возможных пользовательских ролей.

Поля:
- id: UUID pk - уникальный идентификатор.
- name: str - название роли.
- created_at: datetime - дата создания.
- updated_at: datetime - дата обновления.

#### RolePermission
Таблица, в которой указаны ресурс и роль, список возможных действий, которые может совершать пользователь с указанной ролью над указанным ресурсом (булево столбцы, оканчивающиеся на `_permission`).

Поля:
- id: UUID pk - уникальный идентификатор.
- role: fk - ссылка на таблицу Role.
- resource: fk - ссылка на таблицу с ресурсами Resource (apps.resources).
- read_permission: bool - право на чтение.
- read_all_permission: bool - право на чтение списка всех объектов.
- create_permission: bool - право на создание.
- update_permission: bool - право на обновление.
- update_all_permission: bool - право на обновление всех объектов.
- delete_permission: bool - право на удаление.
- delete_all_permission: bool - право на удаление всех объектов.

- created_at: datetime - дата создания.
- updated_at: datetime - дата обновления.

Примечания:
- Для одной пары (role, resource) может существовать только одна запись (уникальность сочетания роли и ресурса).
- Права, оканчивающиеся на `_all_permission`, подразумевают доступ ко всем объектам ресурса (например, чтение/обновление/удаление не только “своих” объектов, но и любых).

#### UserRole
Таблица связи пользователей и ролей (один пользователь может иметь несколько ролей, и одна роль может быть назначена нескольким пользователям).

Поля:
- id: UUID pk - уникальный идентификатор.
- user: fk - ссылка на таблицу User (apps.users).
- role: fk - ссылка на таблицу Role (apps.authorization).
- created_at: datetime - дата создания.
- updated_at: datetime - дата обновления.

Примечания:
- Для одной пары (user, role) может существовать только одна запись (уникальность сочетания пользователя и роли).


#### Логика доступов
При вызове API-методов, выполняющих действия над ресурсами, система проверяет права доступа пользователя к конкретному ресурсу. Пользователь должен быть владельцем ресурса или иметь роль, позволяющую выполнить выбранное действие над этим ресурсом.

Доступ разрешается, если выполняется хотя бы одно условие:
- пользователь является администратором системы (`user.is_admin=True`);
- пользователь является владельцем ресурса (`resource.owner_id == user.id`);
- у пользователя есть хотя бы одна роль, для которой в `RolePermission` для данного `resource` выставлен флаг нужного действия (`*_permission=True`).

Используемые права (флаги в `RolePermission`):
- `read_permission` — чтение объекта.
- `read_all_permission` — чтение списка объектов.
- `create_permission` — создание объекта.
- `update_permission` — обновление объекта.
- `update_all_permission` — обновление любых объектов (не только “своих”).
- `delete_permission` — удаление объекта.
- `delete_all_permission` — удаление любых объектов (не только “своих”).

Пример: получение ресурса по id (`GET /v1/resources/{resource_id}/`).
- Сервис получает `Resource` из БД (если не найден — `404`).
- Если пользователь администратор (`user.is_admin=True`) — доступ разрешается, ресурс возвращается без проверки `RolePermission`.
- Затем вызывается проверка доступа с правом `read_permission`.
- Если доступ не подтверждён — возвращается `403 Нет доступа.`

Пример: получение списка ресурсов (`GET /v1/resources/`, эндпоинт `get_all_resources`).
- Если пользователь администратор (`user.is_admin=True`) — возвращается список всех ресурсов.
- Иначе формируется список доступных ресурсов как объединение:
  - ресурсов, где пользователь является владельцем (`owner_id == user.id`);
  - ресурсов, к которым у одной из ролей пользователя есть право `read_all_permission=True` в `RolePermission`.
- Если итоговый список пуст — возвращается `403 Нет доступа.`

#### Аутентификация и коды ошибок
Аутентификация реализована через JWT (Bearer-токен в заголовке `Authorization: Bearer <token>`).

- `401 Unauthorized` — если по входящему запросу не удалось определить залогиненного пользователя (нет токена / токен невалидный / токен истёк / токен отозван).
- `403 Forbidden` — если пользователь определён, но доступ к запрашиваемому ресурсу отсутствует по правилам выше.
- `404 Not Found` — если ресурс не найден.

#### API для управления правилами доступа (только для администратора)
Администратор системы в текущей реализации определяется флагом `User.is_admin == True` (это не роль из таблицы `Role`).

Доступные методы:
- `GET /v1/authorization/permissions/` — получить список всех правил (`RolePermission`) (только админ).
- `PATCH /v1/authorization/permissions/{permission_id}/` — изменить правило доступа (админ; также владелец ресурса может менять права для своего ресурса).
- `POST /v1/authorization/roles/` — создать роль (только админ).
- `GET /v1/authorization/roles/` — получить список ролей (только админ).
- `POST /v1/authorization/user-roles/` — назначить роль пользователю (только админ).

#### Тестовые данные (для демонстрации системы)
Команда `python manage.py create_test_data` создаёт/обновляет минимальный набор данных:
- Пользователи:
  - `test@test.com` / `testpassword` — обычный пользователь.
  - `owner@test.com` / `testpassword` — владелец ресурса.
  - `admin@test.com` / `adminpassword` — администратор (`is_admin=True`).
- Роль: `Менеджер`.
- Ресурс: `Заказы` (владелец — `owner@test.com`).
- Правило доступа: `RolePermission(Менеджер -> Заказы)` со значениями:
  - `read_permission=True`, `read_all_permission=True`, `create_permission=True`, `update_permission=True`
  - `update_all_permission=False`, `delete_permission=False`, `delete_all_permission=False`
- Связь пользователя и роли: `test@test.com` получает роль `Менеджер`.

Примечание: в API ресурсов сейчас реализован демонстрационный метод `GET /v1/resources/{resource_id}/`, который проверяет `read_permission` (и допуск владельца). Остальные права (`create/update/delete` и варианты `_all_permission`) предусмотрены в модели и API управления правилами и могут быть задействованы при расширении CRUD-методов ресурса.




## Ссылки

##### Сваггер

```
http://localhost:8080/api/docs#/
```

##### Админка Django

```
http://localhost:8080/admin/
```

## Запуск проекта


### Полный запуск проекта с созданием тестовых данных
```shell
make start
```
_____

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
