from datetime import datetime

from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

class CustomUserManager(BaseUserManager):
    """создание менеджера пользователя и модели пользователя,
    наследуемая от AbstractBaseUser"""
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError ('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        print('++++работает метод create_user')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self,email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)  # за отображение в админке
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class ProfileUser(models.Model):
    """описывает профиль пользователя, когда он входит в систему по почте и паролю"""
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='имя пользователя')
    date_birth = models.DateField(blank=True, null=True,verbose_name='дата рождения пользователя')
    info_about_user = models.TextField(blank=True, null=True, verbose_name='информация о пользователе')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def age_user(self):
        """функция возвращает возраст пользователя, по дате рождения"""
        today = datetime.today()
        birth = datetime.strptime(self.date_birth, '%Y-%m-%d')
        age = today.year - birth.year
        if today.month < birth.month or (today.month == birth.month and today.day < birth.day):
            age -= 1

        return age


class UserImage(models.Model):
    user_profile = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/', verbose_name='изображение пользователя')
    is_main = models.BooleanField(default=False)


class NewProduct(models.Model):
    name =models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=5)
