from django.urls import path
from Gallery import views

urlpatterns = [
    path('', views.MediaItemListView.as_view(), name='media_item_list'),
    path('media_item/create/', views.MediaItemCreateView.as_view(), name='media_item_create'),
    path('media_item/<int:pk>/', views.MediaItemDetailView.as_view(), name='media_item_detail'),
    path('media_item/<int:pk>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('media_item/<int:pk>/update/', views.MediaItemUpdateView.as_view(), name='media_item_update'),
    path('media_item/<int:pk>/delete/', views.MediaItemDeleteView.as_view(), name='media_item_delete'),
]
