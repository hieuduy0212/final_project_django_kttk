from django.urls import path
from giaodien import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', view=views.IndexView.as_view()),
    path('create-appointment', view=views.CreateAppointmentView.as_view()),
    path('add-patient', view=views.AddPatientView.as_view()),
    path('list-appointment', view=views.ListAppointmentView.as_view()),
]
