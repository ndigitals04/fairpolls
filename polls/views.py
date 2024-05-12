from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Voter,PollVote, Question, Choice
# Create your views here.
def index(request):
    question_list = Question.objects.all
    context = {
        "question_list": question_list
    }
    return render(request, "polls/index.html", context)