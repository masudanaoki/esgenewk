import uuid as uuid_lib

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, UserManager)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
class BaseModel(models.Model):
    order = models.IntegerField(null=True, blank=True, verbose_name ='表示順')
    created = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name ='作成日時')
    modified = models.DateTimeField(null=True, blank=True, auto_now=True, verbose_name ='更新日時')

    class Meta:
        abstract = True

class Tm_Department(BaseModel):
    department_key = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=200, verbose_name ='部門名')
    def __str__(self):
        return self.department_name

    class Meta:
        db_table = 'Tm_Department'
        verbose_name ='部門マスタ'
        verbose_name_plural = '部門マスタ'

# class UserManager(BaseUserManager):
#     def create_user(self, username, email, password=None):
#         if not username:
#             raise ValueError('Users must have an username')
#         elif not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             username = username,
#             email = self.normalize_email(email),
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password):
#         user = self.create_user(
#             username,
#             email,
#             password=password,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

class User(AbstractBaseUser, PermissionsMixin):
    """ユーザー AbstractUserをコピペし編集"""

    uuid = models.UUIDField(default=uuid_lib.uuid4,
                            primary_key=True, editable=False)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    full_name = models.CharField(_('氏名'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    departments = models.ManyToManyField(
        Tm_Department,
        verbose_name=_('所属'),
        blank=True,
        help_text=_('Specific Tm_Department for this user.'),
        related_name="user_set",
        related_query_name="user",
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
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

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # 既存メソッドの変更
    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.username

class Profile(models.Model):
    CHOICES = (
        ('female', '女性',),
        ('male', '男性',),
        ('not_applicable', '秘密',)
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=CHOICES, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    favorite_words = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'Profile'
        verbose_name ='プロファイル'
        verbose_name_plural = 'プロファイル'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        profile = Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, raw, using, update_fields, **kwargs):
    # if created:
    # try:
        instance.profile.update_or_create()
    # except (ValueError, IndexError, ):
    #     return None
    # except Profile.DoesNotExist:
    #     return None
