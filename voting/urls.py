from django.urls import path

from . import views

app_name = "voting"

urlpatterns = [
    path("", views.PollListView.as_view(), name="list"),
    path("create/", views.PollCreateView.as_view(), name="create"),
    path("<int:pk>/", views.PollDetailView.as_view(), name="detail"),
    path("<int:pk>/vote/", views.vote, name="vote"),
    path("<int:pk>/edit/", views.PollUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.PollDeleteView.as_view(), name="delete"),
]
