import uuid
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

def check_user_id(value):
    if value[0] != '@':
        raise ValidationError('ユーザーIDの先頭には「@」を付けてください')

class Band(models.Model):
    name = models.CharField(_('バンド'), max_length=150, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('バンド')
        verbose_name_plural = _('バンド')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_id, username, password, **extra_fields):
        username = self.model.normalize_username(username)
        user = self.model(user_id=user_id, username=username,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_id, username, password, **extra_fields)

    def create_superuser(self, user_id, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user_id, username, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    # email = models.EmailField(_('email address'), blank=True)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('ユーザー名'),
        max_length=150,
        blank=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        unique=False,
        # error_messages={
        #     'unique': _("A user with that username already exists."),
        # },
    )

    full_name = models.CharField(_('氏名'), max_length=150, blank=False, unique=False)

    user_id = models.CharField(
        _('ユーザーID'),
        max_length=150,
        unique=True,
        validators=[check_user_id],
    )

    band = models.ManyToManyField(
        Band,
        verbose_name=_('所属バンド'),
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    suffrage = models.BooleanField(
        _('投票権'),
        default=True,
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['username', 'full_name']

    class Meta:
        db_table = 'User'
        verbose_name = _('user')
        verbose_name_plural = _('ユーザー')

