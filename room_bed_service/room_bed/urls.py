from django.urls import path
from .views import (
    TypeCreateView, TypeListView,
    RoomCreateView, RoomListView,
    BedCreateView, BedListView
)

urlpatterns = [
    # Type URLs
    path('types/create/', TypeCreateView.as_view(), name='type_create'),
    path('types/', TypeListView.as_view(), name='type_list'),

    # Room URLs
    path('rooms/create/', RoomCreateView.as_view(), name='room_create'),
    path('rooms/', RoomListView.as_view(), name='room_list'),

    # Bed URLs
    path('beds/create/', BedCreateView.as_view(), name='bed_create'),
    path('beds/', BedListView.as_view(), name='bed_list'),
]
