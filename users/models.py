from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password, nickname,*args, **kwargs):
        if not email or not nickname:
            raise ValueError("이메일, 닉네임을 입력하세요")
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,*args, **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password, nickname):
        user = self.create_user(email, password, nickname)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin): # Permission : is_superuser
    nickname = models.CharField('닉네임', max_length=20, unique=True)
    email = models.CharField('이메일', max_length=40, unique=True)
    profile_image = models.ImageField(upload_to='users/profile_image', default='users/blank_profile_image.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = '유저'
        verbose_name_plural =  '유저 목록'