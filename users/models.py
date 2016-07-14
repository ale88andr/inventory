from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.http import request

from employee.models import Organisation


class UserManager(BaseUserManager):
    """
    Custom user manager
    """
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Необходимо указать идентификатор пользователя.')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model, which describes system users
    """
    email = models.EmailField(
        'Электронная почта',
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    username = models.CharField(
        'Идентификатор',
        max_length=40,
        unique=True,
        db_index=True
    )
    created_at = models.DateField(
        'Дата регистрации',
        auto_now_add=True
    )
    is_active = models.BooleanField(
        'Активен',
        default=True
    )
    organisation = models.ForeignKey(
        Organisation,
        verbose_name='Сотрудник организации',
        null=True,
        blank=True
    )
    ip = models.GenericIPAddressField(
        verbose_name='IP адрес',
        null=True,
        blank=True,
    )
    surname = models.CharField(
        'Фамилия',
        max_length=50,
        blank=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=25,
        blank=True
    )
    middle_name = models.CharField(
        'Отчество',
        max_length=25,
        blank=True
    )

    # for backend
    @property
    def is_staff(self):
        return self.is_superuser

    def get_username(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return '{sn} {fn} {mn}'.format(sn=self.surname, fn=self.first_name, mn=self.middle_name)

    @property
    def login(self):
        return self.get_username()

    @property
    def full_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'