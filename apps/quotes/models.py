from __future__ import unicode_literals
from django.db import models
import re


class UserManager(models.Manager):
    def validate(request, postdata):
        print "===  validating user===="
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        DATE_REGEX = re.compile(r'^(19[0-9][0-9]|20[0-2][0-9]|2018)[-/](0?[1-9]|1[0-2])[-/](0?[1-9]|[12][0-9]|3[01])$')

        errors = {}

        if 'name' in postdata:
            if len(postdata['name']) == 0:
                errors['name_length'] = "Error: Name cannot be empty"
            if not re.match('^[\w-]+$', postdata['name']):
                errors['name_char'] = "Error: Name can only be alpha numeric characters"
        if 'alias' in postdata:
            if not re.match('^[\w-]+$', postdata['alias']):
                errors['alias_char'] = "Error: Alias can only be alpha numeric characters"
        if 'email' in postdata:
            if len(postdata['email']) == 0:
                 errors['email_length'] = "Error: Email cannot be empty"               
            if not EMAIL_REGEX.match(postdata['email']):
                errors['email'] = "Error: Email format is incorrect"
        if 'dob' in postdata:
            if len(postdata['dob']) == 0:
                    errors['dob_length'] = "Error: Date of Birth cannot be empty"               
            elif not DATE_REGEX.match(postdata['dob']):
                errors['dob'] = "Error: Date of Birth format is incorrect or out of range"
        if 'pwd' in postdata:
            if (len(postdata['pwd']) < 8):
                errors['password_length'] = "Error: Password has to be longer than 8 characters"
        if 'pwd2' in postdata:
            if postdata['pwd'] != postdata['pwd2']:
                errors['password_match'] = "Error: Password and confirm password must match"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pwd = models.CharField(max_length=255)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __unicode__(self):
        return " id: " + str(self.id) + " name: " + self.name + " alias: " + self.alias + " email: " + self.email + " DOB: " + str(self.dob) + " PWD: " + self.pwd

class QuoteManager(models.Manager):
    def validate_quote(request, q):
        print "===  validating quote"
        errors = {}
        if len(q) == 0:
            errors['quote_length'] = "Error: Quote cannot be empty"
        else:
            try:
                bk = Quote.objects.get(quote=q)
            except Exception as e:
                return errors

            if bk:
                error['quote_exist'] = "Error: Quote already exist."
        return errors

    def validate_author(request, a):
        print "===  validating quote author"
        errors = {}
        if len(a) < 0:
            errors['auth_length'] = "Error: Quote Author cannot be empty"
        return errors

class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="quotes") 
    favorite_of_users = models.ManyToManyField(User, related_name="favorite_quotes") 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()


    def __unicode__(self):
        return "--id: " + str(self.id) + "--Title: " + self.quote + "--Author: " + self.author + "--Fav: " + str(self.favorite_of_users) + "--Creator: " + str(self.creator)
