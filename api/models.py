from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework.authtoken.views import Token

from .constants import *
import datetime


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, firstname, lastname, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            firstname=firstname,
            lastname=lastname,
        )

        user.firstname = user.firstname.capitalize()
        user.lastname = user.lastname.capitalize()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, firstname, lastname, password):
        print("CREATING SUPERUSER")
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            firstname=firstname,
            lastname=lastname,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.firstname = user.firstname.capitalize()
        user.lastname = user.lastname.capitalize()

        user.save(using=self._db)
        # Token.objects.create(user=user)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True, null=False, blank=False)
    firstname = models.CharField(max_length=30, unique=False, null=False, blank=False)
    lastname = models.CharField(max_length=30, unique=False, null=False, blank=False)
    organization_name= models.CharField(max_length=30, unique=False, null=False, blank=False, default="TEST COMPANY")
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    def fullname(self):
        return self.firstname + ' ' + self.lastname

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firstname', 'lastname']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
        

class Broiler(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="broilers")
    date_of_birth = models.DateTimeField()
    animal_bedding_date = models.DateTimeField()
    color = models.CharField(max_length=30, null=False, blank=False)
    gender = models.CharField(max_length=30, null=False, blank=False)
    weight = models.FloatField(null=False, blank=False)
    feed = models.FloatField(null=False, blank=False)
    temperature = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return "BR-" + self.id

    def get_age(self):
        return (datetime.now() - self.date_of_birth).days

    def bedding_duration(self):
        return (datetime.now() - self.animal_bedding_date).days

    def bedding_due(self):
        return (datetime.now() - self.animal_bedding_date).days >= 14

    def is_overweight(self):
        return self.weight >= MAX_WEIGHT

    def is_underweight(self):
        return self.weight <= MIN_WEIGHT

    def is_close_to_being_overweight(self):
        return abs(self.weight - MAX_WEIGHT) == 0.3

    def is_close_to_being_underweight(self):
        return abs(self.weight - MIN_WEIGHT) == 0.3

    def consumes_indadequate_feed(self):
        return self.feed >= MAX_FEED_CONSUMABLE

    def consumes_too_many_feed(self):
        return self.feed <= MIN_FEED_CONSUMABLE

    def is_close_to_being_underfed(self):
        return abs(self.weight - MAX_FEED) == 0.5

    def is_close_to_being_overfed(self):
        return abs(self.weight - MIN_FEED) == 0.5

    def is_cold(self):
        return self.temperature >= MAX_TEMPERATURE

    def is_running_temperature(self):
        return self.temperature <= MIN_TEMPERATURE

    def is_close_to_the_minimum_temperature(self):
        return abs(self.weight - MAX_TEMPERATURE) == 0.5

    def is_close_to_the_maximum_temperature(self):
        return abs(self.weight - MIN_TEMPERATURE) == 0.5
    

class InventoryWeek(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inventory_weeks")
    broilers = models.ForeignKey(Broiler, on_delete=models.CASCADE, related_name="week")
    is_concluded = models.BooleanField(default=False)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    text = models.TextField(null=False, blank=False)
    is_read = models.BooleanField(default=False)
