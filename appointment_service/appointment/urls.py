from django.urls import path
from .views import (
    AppointmentListView,
    AppointmentDetailView,
    AppointmentCreateView,
    AppointmentUpdateView,
    AppointmentDeleteView
)

urlpatterns = [
    path('appointments/', AppointmentListView.as_view(), name='appointment-list'),
    path('appointments/<int:appointment_id>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/create/', AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointments/update/<int:appointment_id>/', AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointments/delete/<int:appointment_id>/', AppointmentDeleteView.as_view(), name='appointment-delete'),
]
