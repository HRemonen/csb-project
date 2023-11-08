from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Choice, Question


@login_required(login_url="/login")
def index_view(request):
    recent_questions = Question.objects.order_by("-pub_date")[:5]

    ctx = {
        "recent_questions": recent_questions,
    }
    return render(request, "securepolls/index.html", ctx)


@csrf_exempt
def register_view(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST["username"], password=request.POST["password"]
        )
        user.save()

        return HttpResponseRedirect(reverse("securepolls:login"))

    return render(request, "securepolls/register.html")


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )

        if user is not None:
            login(request, user)

            return HttpResponseRedirect(reverse("securepolls:index"))

    return render(request, "securepolls/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("securepolls:login"))

@csrf_exempt
def reset_password_view(request):
    if request.method == "POST":
        try:
            user = User.objects.get(username=request.POST["username"])
        except User.DoesNotExist:
            return render(
                request,
                "securepolls/reset_password.html",
                {"error_message": "User does not exist."},
            )
        else:
            user.set_password("password")
            user.save()
            return HttpResponseRedirect(reverse("securepolls:login"))

    return render(request, "securepolls/reset_password.html")


def detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    ctx = {
        "question": question,
    }

    return render(request, "securepolls/detail.html", ctx)


def results_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    ctx = {
        "question": question,
    }

    return render(request, "securepolls/results.html", ctx)


@csrf_exempt
def vote_view(request, question_id):
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
