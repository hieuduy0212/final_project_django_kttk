from django.urls import path
from .views import (
    PatientRecordCreateView,
    PatientRecordUpdateView,
    VisitHistoryCreateView,
    PatientRecordListView,
    PatientRecordDetailView,
    VisitHistoryListView
)

urlpatterns = [
    path('patient_records/create/', PatientRecordCreateView.as_view(), name='patient-record-create'),
    path('patient_records/update/<int:pk>/', PatientRecordUpdateView.as_view(), name='patient-record-update'),
    path('visit_histories/create/', VisitHistoryCreateView.as_view(), name='visit-history-create'),
    path('patient_records/', PatientRecordListView.as_view(), name='patient-record-list'),
    path('patient_records/<int:patient_id>/', PatientRecordDetailView.as_view(), name='patient-record-detail'),
    path('visit_histories/<int:patient_record_id>/', VisitHistoryListView.as_view(), name='visit-history-list'),
]
