from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.utils import timezone
from .models import Voter,PollVote, Question, Choice
from .forms import CreationUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url = "polls:login")
def index(request):
    question_list = Question.objects.all
    context = {
        "question_list": question_list
    }
    return render(request, "polls/index.html", context)

@login_required(login_url = "polls:login")
def questionDetail(request,question_id):
    question = Question.objects.get(pk=question_id)
    if question.closed_date < timezone.now():
        context = {
            "question":question,
            "message":"This poll is closed"
        }
        return render(request,"polls/question_detail.html", context)
    try:
        poll_voted_by_voter = PollVote.objects.get(question=question, voter=request.user.voter)
        print(poll_voted_by_voter)
        if poll_voted_by_voter:
            print("good")
        context = {
            "message":"You have already voted on this poll",
            "question":question
        }
        return render(request, "polls/question_detail.html", context)
    
    except(PollVote.DoesNotExist):
        print("in except clause")
        context = {
            "question": question
        }
        return render(request, "polls/question_detail.html", context)

@login_required(login_url = "polls:login")
def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError,Choice.DoesNotExist):
        context = {
            "question":question,
            "error_message": "You didn't select a choice"
        }
        return render(request, "polls/question_detail.html", context)
        return HttpResponseRedirect(reverse("polls:index"))
    selected_choice.votes = F("votes") + 1
    selected_choice.save()

    poll_voted = PollVote.objects.create(question=question,choice=selected_choice,
                    time_voted= timezone.now(), voter= request.user.voter)
    return HttpResponseRedirect(reverse("polls:voted_success_page", args=(question_id,)))

def votedSuccess(request, question_id):
    return render(request, "polls/succes_vote.html")

@login_required(login_url = "polls:login")
def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    highest_votes = 0
    choiceId = ""
    for choice in question.choice_set.all():
        votes = choice.votes
        if votes > highest_votes:
            highest_votes = votes
            choiceId = choice.id
    winner = Choice.objects.get(pk=choiceId)
    context = {
        "highest_votes":highest_votes,
        "winner":winner,
        "question":question
    }
    return render(request, "polls/result.html", context)

def loginView(request):
    form = CreationUserForm()
    context= {"form":form}

    if request.method == "POST":
        print(request.POST)
        voter_id = request.POST.get("voter_id")
        password = request.POST.get("password")
        user = authenticate(request, username=voter_id, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("polls:index"))
    return render(request, "polls/login.html", context)