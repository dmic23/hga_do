# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.core.files.storage import default_storage
from django.db import models
from django.utils.encoding import smart_unicode
from time import time

def get_upload_file_name(instance, filename):

    return settings.UPLOAD_FILE_PATTERN % (str(time()).replace('.','_'), filename)

class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('Users must have a valid username.')

        user = self.model(
            username=username,
            first_name=kwargs.get('first_name'), last_name=kwargs.get('last_name'),
            email=kwargs.get('email'))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.create_user(username=username, password=password)
        user.username = username
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user

class User(AbstractBaseUser):
    USER_RANK = ( 
        ('1', 'White'),
        ('2', 'Red'),
        ('3', 'Yellow'),
        ('4', 'Green'),
        ('5', 'Blue'),
        ('6', 'Purple'),
        ('7', 'Brown'),
        ('8', 'Black'),
    )
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    user_pic = models.FileField(upload_to=get_upload_file_name, null=True, blank=True, default='blank_user.png')
    user_created = models.DateTimeField(auto_now_add=True)
    user_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_user', null=True, blank=True, unique=False)
    user_updated = models.DateTimeField(auto_now=True)
    user_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_user', null=True, blank=True, unique=False)
    location = models.CharField(max_length=50, null=True, blank=True, default='Ruston')
    play_level = models.CharField(max_length=20, choices=USER_RANK, null=True, blank=True, default='1')

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return smart_unicode(self.username)

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin  


class StudentGoal(models.Model):
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_goal') 
    goal = models.CharField(max_length=250)
    goal_target_date = models.DateTimeField(max_length=50, null=True, blank=True)
    goal_complete = models.BooleanField(default=False)
    goal_complete_date = models.DateTimeField(max_length=50, null=True, blank=True)
    goal_notes = models.TextField(null=True, blank=True)
    goal_created = models.DateTimeField(auto_now_add=True)
    goal_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='goal_created_user')
    goal_updated = models.DateTimeField(auto_now=True)
    goal_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='goal_updated_user', null=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.goal)

class StudentPracticeLog(models.Model):
    PRACTICE_CATEGORIES = ( 
        ('LEAD_TECHNIQUE', 'Lead Technique'),
        ('RHYTHM_TECHNIQUE', 'Rhythm Technique'),
        ('THEORY', 'Theory'),
        ('REPERTOIRE', 'Repertoire'),
        ('APPLIED_THEORY', 'Applied Theory'),
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_log')
    practice_category = models.CharField(max_length=20, choices=PRACTICE_CATEGORIES, null=True, blank=True)
    practice_item = models.CharField(max_length=50)
    practice_time = models.CharField(max_length=50, null=True, blank=True)
    practice_speed = models.CharField(max_length=50, null=True, blank=True)
    practice_notes = models.TextField(null=True, blank=True)
    practice_date = models.DateTimeField(max_length=50, null=True, blank=True)
    practice_item_created = models.DateTimeField(auto_now_add=True)
    practice_item_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='log_created_user')
    practice_item_updated = models.DateTimeField(auto_now=True)
    practice_item_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='log_updated_user', null=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.practice_item)

class StudentObjective(models.Model):

    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_objective')
    objective = models.CharField(max_length=250)
    objective_complete = models.BooleanField(default=False)
    objective_complete_date = models.DateTimeField(max_length=50, null=True, blank=True)
    objective_notes = models.TextField(null=True, blank=True)
    objective_created = models.DateTimeField(auto_now_add=True)
    objective_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='objective_created_user')
    objective_updated = models.DateTimeField(auto_now=True)
    objective_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='objective_updated_user', null=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.objective)

class StudentWishList(models.Model):

    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_wishlist')
    wish_item = models.CharField(max_length=250)
    wish_item_complete = models.BooleanField(default=False)
    wish_item_complete_date = models.DateTimeField(max_length=50, null=True, blank=True)
    wish_item_notes = models.TextField(null=True, blank=True)
    wish_item_created = models.DateTimeField(auto_now_add=True)
    wish_item_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='wish_item_created_user')
    wish_item_updated = models.DateTimeField(auto_now_add=True)
    wish_item_updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='wish_item_updated_user', null=True, blank=True)

    def __unicode__(self):
        return smart_unicode(self.wish_item)

class StudentMaterial(models.Model):

    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student_material')
    file = models.FileField(upload_to=get_upload_file_name, null=True, blank=True)
    material_name = models.CharField(max_length=50, null=True, blank=True)
    material_notes = models.TextField(null=True, blank=True)
    material_added = models.DateTimeField(auto_now_add=True)
    material_added_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='material_added_user')

