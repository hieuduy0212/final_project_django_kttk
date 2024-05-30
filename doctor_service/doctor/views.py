from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Specialist, Doctor, Department
from .serializers import SpecialistSerializer, DoctorSerializer, DepartmentSerializer

# Views for Specialist
class SpecialistList(APIView):
    def get(self, request):
        specialists = Specialist.objects.all()
        serializer = SpecialistSerializer(specialists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SpecialistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentList(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecialistDetail(APIView):
    def get_object(self, pk):
        try:
            return Specialist.objects.get(pk=pk)
        except Specialist.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        specialist = self.get_object(pk)
        serializer = SpecialistSerializer(specialist)
        return Response(serializer.data)

    def put(self, request, pk):
        specialist = self.get_object(pk)
        serializer = SpecialistSerializer(specialist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        specialist = self.get_object(pk)
        specialist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DepartmentDetail(APIView):
    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def put(self, request, pk):
        department = self.get_object(pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = self.get_object(pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views for Doctor
class DoctorList(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorDetail(APIView):
    def get_object(self, pk):
        try:
            return Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doctor = self.get_object(pk)
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
