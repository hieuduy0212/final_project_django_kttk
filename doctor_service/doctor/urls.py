from django.urls import path
from .views import SpecialistList, SpecialistDetail, DoctorList, DoctorDetail, DepartmentList

urlpatterns = [
    # URLs for Specialist
    path('specialists/', SpecialistList.as_view(), name='specialist-list'),
    path('specialists/<int:pk>/', SpecialistDetail.as_view(), name='specialist-detail'),

    path('departments/', DepartmentList.as_view(), name='specialist-list'),
    path('departments/<int:pk>/', SpecialistDetail.as_view(), name='specialist-detail'),

    # URLs for Doctor
    path('doctors/', DoctorList.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetail.as_view(), name='doctor-detail'),
]
