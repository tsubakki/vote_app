import uuid
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django_mysql.models import ListCharField

def check_vote_num(value):
    if value < 0:
        raise ValidationError('マイナスの値は設定できません')

def check_auth_key(value):
    f = open('auth_key.txt', 'r')
    auth_key = f.read()
    if value != auth_key:
        raise ValidationError('認証キーが違います')

def check_vote_setting(value):
    vote = Vote.objects.all()
    print("ここ")
    print(vote)
    if len(vote) == 1:
        if vote[0].uuid != value:
            raise ValidationError('すでに設定が存在しています')


class Band(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, 
        primary_key=True, 
        editable=False
    )

    name = models.CharField(
        _('バンド名'), 
        max_length=150, 
        blank=False, 
        unique=True
    )

    is_first_grade_band = models.BooleanField(
        _('一年生バンド'),
        default=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('バンド')
        verbose_name_plural = _('バンド')

class Vote(models.Model):

    uuid = models.UUIDField(
        _('設定ID(変更しないでください)'),
        validators=[check_vote_setting],
        default=uuid.uuid4, 
        primary_key=True,
        blank=False,
        )
 
    band_num = models.IntegerField(
        _('通過バンド数(一年生バンド数を含む)'),
        validators=[check_vote_num],
        default=7,
    )

    first_grade_band_num = models.IntegerField(
        _('一年生バンド数'),
        validators=[check_vote_num],
        default=1,
    )
    
    pass_band = ListCharField(
        base_field=models.CharField(max_length=150),
        size=50,
        max_length=(50 * 151),
        blank=True,
        editable=False,
    )

    is_active = models.BooleanField(
        _('投票中'),
        default=False,
    )

    announce = models.BooleanField(
        _('結果の公開'),
        default=False,
    )

    date_joined = models.DateTimeField(
        _('作成日'),
        auto_now=True)
    
    def __str__(self):
        date = str(self.date_joined)
        return '{}年{}月{}日 {}時{}分{}秒'.format(date[:4],date[5:7],date[8:10],date[11:13],date[14:16],date[17:19])
    
    class Meta:
        verbose_name = _('投票設定')
        verbose_name_plural = _('投票設定')


class UserManager(BaseUserManager):
    # use_in_migrations = True
    def _create_user(self, user_id, full_name, auth_key, password, **extra_fields):
        user = self.model(user_id=user_id, full_name=full_name, auth_key=auth_key, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, full_name, auth_key, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_id, full_name, auth_key, password, **extra_fields)

    def create_superuser(self, user_id, full_name, auth_key, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user_id, full_name, auth_key, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    full_name = models.CharField(
        _('氏名'), 
        max_length=150, 
        blank=False, 
        unique=False
    )

    user_id = models.CharField(
        _('ユーザーID'),
        max_length=150,
        unique=True,
    )

    auth_key = models.CharField(
        _('認証キー'), 
        max_length=150, 
        validators=[check_auth_key],
    )

    band = models.ManyToManyField(
        Band,
        verbose_name=_('所属バンド'),
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )

    vote_contents = ListCharField(
        base_field=models.CharField(max_length=150),
        size=50,
        max_length=(50 * 151),
        blank=True,
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    suffrage = models.BooleanField(
        _('投票権'),
        default=False,
    )

    vote_finish = models.BooleanField(
        _('投票済'),
        default=False,
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
    )
    
    date_joined = models.DateTimeField(
        _('date joined'), 
        default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['full_name','auth_key']

    class Meta:
        db_table = 'User'
        verbose_name = _('user')
        verbose_name_plural = _('ユーザー')

