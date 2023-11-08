from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .models import Choice, User, Question


def index(request):
    recent_questions = Question.objects.order_by("-pub_date")[:5]

    ctx = {
        "recent_questions": recent_questions,
    }
    return render(request, "securepolls/index.html", ctx)


@csrf_exempt
def register(request):
    if request.method == "POST":
        user = User(
            username=request.POST["username"], password=request.POST["password"]
        )
        user.save()

    return render(request, "securepolls/register.html")


@csrf_exempt
def login(request):
    if request.method == "POST":
        user = User.objects.get(username=request.POST["username"])

        if not user or request.POST["password"] != request.POST["password"]:
            return render(request, "pages/login.html")

        return HttpResponseRedirect(reverse("securepolls:index"))

    return render(request, "securepolls/login.html")


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    ctx = {
        "question": question,
    }

    return render(request, "securepolls/detail.html", ctx)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    ctx = {
        "question": question,
    }

    return render(request, "polls/results.html", ctx)


@csrf_exempt
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "securepolls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("securepolls:results", args=(question.id,)))
