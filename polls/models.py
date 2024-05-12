from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
    name = models.CharField(max_length=200, null=True)
    pub_date =models.DateTimeField("date published", auto_now_add=True)
    closed_date = models.DateTimeField("Date closed")

    def __str__(self):
        return self.name
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, null=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    voter_id= models.CharField(max_length=40, null=True)
    email = models.EmailField(null=True)
    
    def __str__(self):
        return self.voter_id

class PollVoted(models.Model):
    question_voted_on = models.ForeignKey(Question, on_delete=models.SET_NULL, blank=True, null=True)
    choice_voted = models.ForeignKey(Choice,on_delete=models.SET_NULL, blank=True, null=True)
    time_voted = models.DateTimeField()

    def __str__(self):
        return self.question_voted_on
