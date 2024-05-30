from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, FullNameSerializer
from .models import User
import jwt, datetime
from django.utils.decorators import method_decorator
from django.conf import settings

class RegisterView(APIView):
  def post(self, request):
    data = request.data
    full_name_serializer = FullNameSerializer(data={
      'first_name': data.get('first_name'),
      'mid_name': data.get('mid_name'),
      'last_name': data.get('last_name')
    })

    if full_name_serializer.is_valid():
      full_name = full_name_serializer.save()
    else:
      return Response(full_name_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user_serializer = UserSerializer(data={
      'email': data.get('email'),
      'password': data.get('password'),
      'full_name': FullNameSerializer(full_name).data
    })
    print(user_serializer.is_valid())
    print(user_serializer.errors)
    if user_serializer.is_valid():
      user_serializer.save()
      return Response({'message': 'Đăng ký thành công'}, status=status.HTTP_201_CREATED)
    else:
      full_name.delete()
      return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
  def post(self, request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()

    if user is None:
      raise AuthenticationFailed('User not found')

    if not user.check_password(password):
      raise AuthenticationFailed('Incorrect password')

    payload = {
      'id': user.id,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
      'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response['Authorization'] = 'Bearer ' + token
    response.data = {
      'jwt': token
    }

    return response

class UserView(APIView):
  def get(self, request):
    token = request.COOKIES.get('jwt')

    if not token:
      raise AuthenticationFailed('Unauthenticated')

    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Unauthenticated')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)

    return Response(serializer.data)

class LogoutView(APIView):
  def post(self, request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
      'message': 'success'
    }
    return response

def jwt_required():
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return JsonResponse({'error': 'Authorization header not found'}, status=401)

            try:
                token_type, token = auth_header.split(' ')
                if token_type != 'Bearer':
                    raise ValueError('Invalid token type')
            except (ValueError, IndexError):
                return JsonResponse({'error': 'Invalid authorization header'}, status=401)

            try:
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token['id']
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'JWT is expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid JWT'}, status=401)

            kwargs['user_id'] = user_id
            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator

class UpdateUserView(APIView):

    @method_decorator(jwt_required())
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        request.data["email"] = user.email
        serializer = UserSerializer(user, data=request.data, partial=True)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
