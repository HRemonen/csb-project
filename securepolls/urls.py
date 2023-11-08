from django.urls import path

from . import views

app_name = "securepolls"
urlpatterns = [
    path("", views.index, name="index"),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
