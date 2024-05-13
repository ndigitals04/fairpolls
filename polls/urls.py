from django.urls import path
from . import views

app_name= "polls"
urlpatterns = [
    path('',views.index, name="index"),
    path('<int:question_id>/',views.questionDetail, name="question_detail"),
    path('<int:question_id>/vote',views.vote, name="vote"),
    path('<int:question_id>/voted',views.votedSuccess, name="voted_success_page"),
]
