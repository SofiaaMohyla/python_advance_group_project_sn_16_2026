from django.urls import path
from events import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event-list'),
    path('detail/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('create/', views.EventCreateView.as_view(), name='event-create'),
    path('update/<int:pk>/', views.EventUpdateView.as_view(), name='event-update'),
    path('delete/<int:pk>/', views.EventDeleteView.as_view(), name='event-delete'),
]