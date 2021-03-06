from django.db import models
import random
import datetime
from django.utils import timezone
from django import forms

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
def __unicode__(self):
     return self.question_text
class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
def __unicode__(self):
    return self.choice_text
class auth_user(models.Model):
	username = models.CharField(max_length=30)
	password=models.CharField(max_length=128)