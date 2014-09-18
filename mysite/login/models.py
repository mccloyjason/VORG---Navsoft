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
class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)
	password=forms.CharField(label='Password', max_length=100)
