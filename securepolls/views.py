from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Question


def index(request):
    recent_questions = Question.objects.order_by("-pub_date")[:5]

    ctx = {
        "recent_questions": recent_questions,
    }
    return render(request, "securepolls/index.html", ctx)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    ctx = {
        "question": question,
    }

    return render(request, "securepolls/detail.html", ctx)


def results(request, question_id):
    return HttpResponse(f"You're looking at the results of question {question_id}.")


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")
