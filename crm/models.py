from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Create your models here.


class User(AbstractUser):

    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=30, unique=False)
    last_name = models.CharField(max_length=30, unique=False)
    is_admin = models.BooleanField(default=False)
    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=30)
    bio = models.CharField(max_length=200)
    def __str__(self):
        return self.user.email

class Lead(models.Model):

    # Defines Choices
    # Lead Status
    NEW_LEAD = 'New Lead'
    WON = 'Won'
    LOST = 'Lost'
    FOLLOW_UP = 'Follow Up'

    
    STATUSLIST = [
        (NEW_LEAD, _('New Lead')),
        (WON, _('Won')),
        (LOST, _('Lost')),
        (FOLLOW_UP, _('Follow Up')),
    ]

    #Lead Intent
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'

    INTENT_RANGE = [
        (LOW,_('Low')),
        (MEDIUM,_('Medium')),
        (HIGH,_('High')),
    ]

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=60)
    contact_num = models.IntegerField()
    touches = models.IntegerField()
    last_contacted = models.DateField()
    date_created = models.DateField()
    status = models.CharField(choices=STATUSLIST, max_length=20)
    intent = models.CharField(choices=INTENT_RANGE, max_length=20)
    notes = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name + self.last_name
