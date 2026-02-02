from __future__ import annotations

import bcrypt
from django.core.management.base import BaseCommand
from django.db import transaction
from typing import Optional

from apps.authorization.models import Role, RolePermission, UserRole
from apps.resources.models import Resource
from apps.users.models import User


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


class Command(BaseCommand):
    requires_system_checks: list[str] = []
    requires_migrations_checks = False

    help = (
        'Создаёт тестовые данные для локального запуска/проверки проекта: '
        'пользователей, роль, ресурс, права доступа и связь пользователь-роль. '
    )

    @transaction.atomic
    def handle(self, *args, **options):

        test_password = 'testpassword'

        owner_user = self._create_user(
            email='owner@test.com',
            password=test_password,
            first_name='Василий',
            last_name='Васильев',
            patronymic='Васильевич',
        )

        test_user = self._create_user(
            email='test@test.com',
            password=test_password,
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович',
        )

        admin_user = self._create_user(
            email='admin@test.com',
            password='adminpassword',
            first_name='Админ',
            last_name='Системы',
            is_admin=True,
        )

        role, _ = Role.objects.get_or_create(name='Менеджер')

        resource, resource_created = Resource.objects.get_or_create(
            name='Заказы',
            defaults={'owner': owner_user},
        )
        if not resource_created and resource.owner_id != owner_user.id:
            resource.owner = owner_user
            resource.save(update_fields=['owner'])

        permission_defaults = {
            'read_permission': True,
            'read_all_permission': True,
            'create_permission': True,
            'update_permission': True,
            'update_all_permission': False,
            'delete_permission': False,
            'delete_all_permission': False,
        }
        role_permission, _ = RolePermission.objects.get_or_create(
            role=role,
            resource=resource,
            defaults=permission_defaults,
        )

        UserRole.objects.get_or_create(user=test_user, role=role)

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            'Тестовые данные созданы/обновлены.'))
        self.stdout.write('Пользователи и их пароли:')
        self.stdout.write(f'- test@test.com / {test_password}')
        self.stdout.write(f'- owner@test.com / {test_password}')
        self.stdout.write('- admin@test.com / adminpassword (is_admin=True)')
        self.stdout.write('')
        self.stdout.write('Роли и ресурсы:')
        self.stdout.write("- Роль: 'Менеджер'")
        self.stdout.write("- Ресурс: 'Заказы'")
        self.stdout.write('- Право: RolePermission(Менеджер - Заказы) создано')
        self.stdout.write('')

    @staticmethod
    def _create_user(
        *,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        patronymic: Optional[str] = '',
        is_admin: bool = False,
        is_active: bool = True,
    ) -> User:
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={
                'password_hash': _hash_password(password),
                'first_name': first_name,
                'last_name': last_name,
                'patronymic': patronymic,
                'is_admin': is_admin,
                'is_active': is_active,
            }
        )

        return user
