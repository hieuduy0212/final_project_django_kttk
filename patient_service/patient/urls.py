from django.urls import path
from .views import PatientListView, PatientDetailView, PatientCreateView, PatientUpdateView, PatientDeleteView

urlpatterns = [
    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/<int:patient_id>/', PatientDetailView.as_view(), name='patient-detail'),
    path('patients/create/', PatientCreateView.as_view(), name='patient-create'),
    path('patients/<int:patient_id>/update/', PatientUpdateView.as_view(), name='patient-update'),
    path('patients/<int:patient_id>/delete/', PatientDeleteView.as_view(), name='patient-delete'),
]
