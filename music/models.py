from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.authtoken.models import Token


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")

        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        Token.objects.create(user=user)
        return user

    def create_superuser(self, email, password):

        if not (email or password):
            raise ValueError("Super user must have an email and password")
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()


class User(AbstractBaseUser):
    """this class represents the user Model.
    """

    class Meta:
        db_table = 'users'
        managed = True

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, unique=True)
    country_code = models.IntegerField(blank=True, null=True)
    contact_no = models.BigIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __unicode__(self):
        return self.email

    def get_my_token(self):
        return Token.objects.get(user=self.objects)


class Genre(models.Model):
    class Meta:
        db_table = 'genre'

    user = models.ForeignKey(User, default=1)
    genre = models.CharField(max_length=100)
    is_favorite = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.genre


class Song(models.Model):
    class Meta:
        db_table = 'songs'

    user = models.ForeignKey(User, default=1)
    song_title = models.CharField(max_length=250)
    genre = models.CharField(max_length=100)
    audio_file = models.FileField(default='')
    ratings = models.IntegerField(default=0,
                                  validators=[MaxValueValidator(5), MinValueValidator(0)])
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
