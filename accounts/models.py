from django.db.models import EmailField, CharField, BooleanField, DateTimeField
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, identify_hasher


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, name=None, full_name=None,
                    is_active=True, is_staff=None, is_admin=None):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('Користувач повинен мати електронну адресу')
        if not password:
            raise ValueError('Користувач повинен ввести пароль')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password,
                                is_staff=True, is_admin=True)
        return user

    def create_staffuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password,
                                is_staff=True, is_admin=False)
        return user


class User(AbstractBaseUser):
    email = EmailField(unique=True, max_length=255)
    name = CharField(max_length=255, blank=True, null=True)
    full_name = CharField(max_length=255, blank=True, null=True)
    staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    admin = BooleanField(default=False)
    timestamp = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'  # запрашиваемое поле для автаризации
    REQUIRED_FIELDS = []  # ніякі додаткові поля для авторизаціі не будуть запрашиватся

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_short_name(self):  # функція виводить eml замість імя якщо його немає
        if self.name:
            return self.name
        return self.email

    def get_full_name(self):  # функція виводить eml замість повного імя якщо його немає
        if self.full_name:
            return self.full_name
        return self.email

    def has_perm(self, perm, obj=None):  # відповідає за права на обєкти в адмінке
        return True

    def has_module_perms(self, app_label):  # права на модуль
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_amin(self):
        return self.admin

    def save(self, *args, **kwargs):
        try:
            _alg = identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
