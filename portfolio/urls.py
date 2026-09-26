from django.urls import path
from portfolio import views

urlpatterns = [
    path('', views.PortfListView.as_view(), name='portfolio-list'),
    path('create/', views.PortfCreateView.as_view(), name='portfolio-create'),
    path('update/<int:pk>/', views.PortfUpdateView.as_view(), name='portfolio-update'),
    path('detail/<int:pk>/', views.PortfDetailView.as_view(), name='portfolio-detail'),
    path('delete/<int:pk>/', views.PortfDeleteView.as_view(), name='portfolio-delete'),
    path('comment/create/<int:pk>/', views.CommentCreateView.as_view(), name='comment-create'),
]