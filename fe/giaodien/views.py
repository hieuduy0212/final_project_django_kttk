from django.shortcuts import render
from django.views import View
from django.http import HttpRequest

class IndexView(View):
    def get(self, request):
        return render(request=request, template_name='index.html', content_type='text/html')

class CreateAppointmentView(View):
    def get(self, request):
        return render(request=request, template_name='create_appointment.html', content_type='text/html')

class AddPatientView(View):
    def get(self, request):
        return render(request=request, template_name='add_patient.html', content_type='text/html')

class ListAppointmentView(View):
    def get(self, request):
        return render(request=request, template_name='list_appointment.html', content_type='text/html')
