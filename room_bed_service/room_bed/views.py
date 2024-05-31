from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Type, Room, Bed
from .serializers import TypeSerializer, RoomSerializer, BedSerializer

# Type Views
class TypeCreateView(APIView):
    def post(self, request):
        serializer = TypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TypeListView(APIView):
    def get(self, request):
        types = Type.objects.all()
        serializer = TypeSerializer(types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Room Views
class RoomCreateView(APIView):
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomListView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Bed Views
class BedCreateView(APIView):
    def post(self, request):
        serializer = BedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BedListView(APIView):
    def get(self, request):
        beds = Bed.objects.all()
        serializer = BedSerializer(beds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
