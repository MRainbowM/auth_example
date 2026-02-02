
.DEFAULT_GOAL := help

COMPOSE ?= docker compose -f docker-compose.yml

# Дефолтные учетные данные суперпользователя (можно переопределить: make start DJANGO_SUPERUSER_PASSWORD=...)
DJANGO_SUPERUSER_USERNAME ?= admin
DJANGO_SUPERUSER_EMAIL ?= admin@example.com
DJANGO_SUPERUSER_PASSWORD ?= admin

.PHONY: help start env docker-up backend-run superuser test-data stop down logs

help:
	@echo "Доступные команды:"
	@echo "  make start    - поднять проект, создать суперпользователя и тестовые данные"
	@echo "  make stop     - остановить контейнеры (без удаления данных)"
	@echo "  make down     - остановить и удалить контейнеры (c volumes)"
	@echo "  make logs     - логи docker compose"

# Полный старт проекта.
start: env docker-up backend-run superuser test-data
	@echo ""
	@echo "Готово."
	@echo "Админка: http://localhost:8080/admin/"
	@echo "Swagger: http://localhost:8080/api/docs#/"
	@echo ""

# Создать .env с дефолтами (если его нет).
env:
	@if [ ! -f .env ]; then \
		echo "Создаю .env из .env.example"; \
		cp .env.example .env; \
	fi
	@# Добавляем учетные данные суперюзера в .env, если их там ещё нет (не трогаем если уже заданы)
	@grep -q '^DJANGO_SUPERUSER_USERNAME=' .env || printf '\nDJANGO_SUPERUSER_USERNAME=%s\n' "$(DJANGO_SUPERUSER_USERNAME)" >> .env
	@grep -q '^DJANGO_SUPERUSER_EMAIL=' .env || printf 'DJANGO_SUPERUSER_EMAIL=%s\n' "$(DJANGO_SUPERUSER_EMAIL)" >> .env
	@grep -q '^DJANGO_SUPERUSER_PASSWORD=' .env || printf 'DJANGO_SUPERUSER_PASSWORD=%s\n' "$(DJANGO_SUPERUSER_PASSWORD)" >> .env

docker-up:
	@$(COMPOSE) up --build -d

# В docker-compose.yml backend не стартует сервер сам,
# поэтому запускаем uvicorn отдельным процессом внутри контейнера.
backend-run:
	@$(COMPOSE) exec -T backend python -c "import socket; s=socket.socket(); s.settimeout(0.2); ok = (s.connect_ex(('127.0.0.1', 8006)) == 0); s.close(); raise SystemExit(0 if ok else 1)" >/dev/null 2>&1 && \
		echo "uvicorn уже запущен на :8006" || \
		$(COMPOSE) exec -d backend python -m uvicorn config.asgi:application --reload --host 0.0.0.0 --port 8006

# Создать/обновить суперпользователя Django (idempotent) и вывести логин/пароль.
superuser:
	@echo ""
	@echo "Суперпользователь Django для админки:"
	@echo "  login:    $(DJANGO_SUPERUSER_USERNAME)"
	@echo "  password: $(DJANGO_SUPERUSER_PASSWORD)"
	@$(COMPOSE) exec -T \
		-e DJANGO_SUPERUSER_USERNAME="$(DJANGO_SUPERUSER_USERNAME)" \
		-e DJANGO_SUPERUSER_EMAIL="$(DJANGO_SUPERUSER_EMAIL)" \
		-e DJANGO_SUPERUSER_PASSWORD="$(DJANGO_SUPERUSER_PASSWORD)" \
		backend python manage.py shell -c "\
import os; \
from django.contrib.auth import get_user_model; \
User = get_user_model(); \
username = os.environ['DJANGO_SUPERUSER_USERNAME']; \
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', ''); \
password = os.environ['DJANGO_SUPERUSER_PASSWORD']; \
u, created = User.objects.get_or_create(username=username, defaults={'email': email}); \
u.email = email; \
u.is_staff = True; \
u.is_superuser = True; \
u.set_password(password); \
u.save(); \
print('Superuser ready:', u.username) \
"


test-data:
	@$(COMPOSE) exec -T backend python manage.py create_test_data

stop:
	@$(COMPOSE) stop

down:
	@$(COMPOSE) down -v

logs:
	@$(COMPOSE) logs -f --tail=200
