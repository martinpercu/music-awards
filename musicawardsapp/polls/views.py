from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice

# Create your views here.
def index(request):
    latest_question_list = Question.objects.all()
    return render(request, "polls/index.html", {
        "latest_question_list": latest_question_list
    })
    


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {
        "question": question
    })


def result(request, question_id):
    return HttpResponse(f'You are looking the result N° {question_id}')



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You don't choose an answer. Please do it"            
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:result", args=(question.id,)))






