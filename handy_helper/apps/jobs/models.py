from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validations(self, post_data):
        errors={}
        first_name = self.validate_first_name(post_data, errors)
        last_name = self.validate_last_name(post_data, errors)
        email = self.validate_email(post_data, errors)
        password = self.validate_password(post_data, errors)
        confirm_password = self.validate_password_confirmation(post_data, errors)
        return {**first_name, **last_name, **email, **password, **confirm_password}

    def validate_first_name(self, post_data, errors):
        if len(post_data['first_name']) < 1:
            errors['first_name'] = "First name cannot be empty"
        elif len(post_data['first_name']) < 2:
            errors['first_name'] = "First name must contain at least two letters"
        else: 
            for s in post_data['first_name']:
                if not s.isalpha() and s!='-':
                    errors['first_name'] = "First name must only include letters or '-'"
                    break
        return errors

    def validate_last_name(self, post_data, errors):
        if len(post_data['last_name']) < 1:
            errors['last_name'] = "Last name cannot be empty"
        elif len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must contain at least two letters"
        else: 
            for s in post_data['last_name']:
                if not s.isalpha() and s!='-':
                    errors['last_name'] = "Last name must only include letters or '-'"
                    break
        return errors

    def validate_email(self, post_data, errors):
        if len(post_data['email']) < 1:
            errors['email'] = "Email cannot be empty"
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Invalid email address'
        else: 
            email = User.objects.filter(email=post_data['email'])
            if len(email) > 0: 
                errors['email'] = 'Email address already exists'
        return errors

    def validate_password(self, post_data, errors):
        if len(post_data['password']) < 1:
            errors['password'] = "Password cannot be empty"
        elif len(post_data['password']) < 9:
            errors['password'] = "Password must contain more than 8 characters"
        else:
            up = False
            num = False
            for s in post_data['password']:
                if s.isupper(): up = True
                if s.isdigit(): num = True
            if not up:
                errors['password'] = "Password must contain at least one uppercase letter"
            elif not num:
                errors['password'] = "Password must contain at least one numerical value"
        return errors
            
    def validate_password_confirmation(self, post_data, errors):
        if len(post_data['confirm_pw']) < 1:
            errors['confirm_pw'] = "Confirm password cannot be empty"
        elif post_data['confirm_pw'] != post_data['password']:
            errors['confirm_pw'] = "Confirm password is not the same as password"
        return errors

    def signin_validations(self, post_data):
        errors={}
        email = self.validate_signin_email(post_data, errors)
        password = self.validate_signin_password(post_data, errors)
        return {**email, **password}

    def validate_signin_email(self, post_data, errors):
        if len(post_data['signin_email']) < 1:
            errors['signin_email'] = "Email cannot be empty"
        elif not EMAIL_REGEX.match(post_data['signin_email']):
            errors['signin_email'] = 'Invalid email address'
        else:
            user = User.objects.filter(email=post_data['signin_email'])
            if len(user) < 1: 
                errors['signin_email'] = 'Incorrect email address'
        return errors

    def validate_signin_password(self, post_data, errors):
        if len(post_data['signin_password']) < 1:
            errors['signin_password'] = "Password cannot be empty"
        else:
            user = User.objects.filter(email=post_data['signin_password'])
            if len(user)>0:
                if not bcrypt.checkpw(post_data['signin_password'].encode(), user[0].password_hash.encode()): 
                    errors['signin_password'] = "Incorrect password"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class JobManager(models.Manager):
    def job_validations(self, post_data):
        errors={}
        title = self.validate_title(post_data, errors)
        description = self.validate_description(post_data, errors)
        location = self.validate_location(post_data, errors)
        return {**title, **description, **location}

    def validate_title(self, post_data, errors):
        if len(post_data['title']) < 1:
            errors['title'] = "Title cannot be empty"
        elif len(post_data['title']) < 3:
            errors['title'] = "Title must contain at least three characters"
        else: 
            for s in post_data['title']:
                if not s.isalpha() and s!='-' and s!=" ":
                    errors['title'] = "Title must only include letters or '-'"
                    break
        return errors

    def validate_description(self, post_data, errors):
        if len(post_data['description']) < 1:
            errors['description'] = "Description name cannot be empty"
        elif len(post_data['description']) < 3:
            errors['description'] = "Description must contain at least three letters"
        return errors

    def validate_location(self, post_data, errors):
        if len(post_data['location']) < 1:
            errors['location'] = "Location name cannot be empty"
        elif len(post_data['location']) < 3:
            errors['location'] = "Location must contain at least three letters"
        return errors

class Job(models.Model):
    created_by = models.ForeignKey(User, related_name='created_job', on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, related_name='added_jobs', null=True)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()

    def __str__(self) -> str:
        return f"{self.title}"