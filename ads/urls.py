from django.urls import path
from .views import (
    AdvertisementListView,
    AdvertisementCreateView,
    AdvertisementUpdateView,
    AdvertisementDeleteView,
)

urlpatterns = [
    path(
        '',
        AdvertisementListView.as_view(),
        name='advertisement_list'
    ),

    path(
        'create/',
        AdvertisementCreateView.as_view(),
        name='advertisement_create'
    ),

    path(
        'edit/<int:pk>/',
        AdvertisementUpdateView.as_view(),
        name='advertisement_edit'
    ),

    path(
        'delete/<int:pk>/',
        AdvertisementDeleteView.as_view(),
        name='advertisement_delete'
    ),
]