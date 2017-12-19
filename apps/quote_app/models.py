# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validation(self, postData):
        errors = []

        if len(postData['first_name']) < 2:
            errors.append("First name must be at least 2 letters long")
        elif not postData['first_name'].isalpha():
            errors.append("First name must contain letters only")

        if len(postData['last_name']) < 2:
            errors.append("Last name must be at least 2 letters long")
        elif not postData['last_name'].isalpha():
            errors.append("Last name must contain letters only")
        
        if len(postData['password']) < 8:
            errors.append("Password must be 8 characters long")
        elif postData['password'] != postData['passwordcf']:
            errors.append("Password does not match")
        
        if not postData['birthday']:
            errors.append("Birthday field required")

        if not EMAIL_REGEX.match(postData['email'].lower()):
            errors.append("Email is not valid")
        elif not errors and User.objects.filter(email = postData['email'].lower()):
            errors.append("Email already registered")
        
        return errors
    
    def new_user(self, postData):
        hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())

        return User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], birthday = postData['birthday'], password = hash1)
    
    def login_validation(self, postData):
        errors = []
        users = self.filter(email = postData['email'])  
        if not users:
            errors.append("Email does not exist")
        
        else:
            user = users[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append("Password does not exist")
        
        if not errors:
            return user

        return errors

class QuoteManager(models.Manager):
    def quote_validation(self, postData):
        errors = []
        if len(postData['author']) < 3:
            errors.append("Quoted by must be more than 3 characters")
        
        if len(postData['quote']) < 10:
            errors.append("Messages must be more than 10 characters")
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField()

    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length = 255)
    quote = models.CharField(max_length = 255)
    user = models.ForeignKey(User, related_name="user_submission")
    favorite = models.ManyToManyField(User, related_name= "user_favorites")

    objects = QuoteManager()
        