from django.urls import path

from . import views

app_name = "securepolls"
urlpatterns = [
    path("", views.index_view, name="index"),
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path("<int:question_id>/", views.detail_view, name="detail"),
    path("<int:question_id>/results/", views.results_view, name="results"),
    path("<int:question_id>/vote/", views.vote_view, name="vote"),
]
