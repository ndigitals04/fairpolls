from django.contrib import admin
from .models import Voter, PollVote, Question,Choice
# Register your models here.

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(PollVote)