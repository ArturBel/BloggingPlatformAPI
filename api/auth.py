from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# helper function to get tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user=user)
    return {'access': str(refresh.access_token), 'refresh': str(refresh)}


@api_view(['POST'])
def register(request):
    # creating a new user from json data
    user_serializer = UserSerializer(data=request.data)

    # checking if prohibited fields are not present (or false)
    if request.data.get('is_staff') is True or request.data.get('is_superuser') is True:
        return Response(data={'msg': 'You do not have permission to register as superuser or staff.'}, status=status.HTTP_401_UNAUTHORIZED)

    # checking if json data is valid
    if user_serializer.is_valid():
        # hashing the password before storing in the database
        new_user = user_serializer.save()
        
        # saving new user, generation tokens and outputting result
        new_user.save()
        tokens = get_tokens_for_user(user=new_user)
        return Response(data={**user_serializer.data, 'msg': 'Registration successful', 'tokens': tokens}, status=status.HTTP_201_CREATED)
    else:
        return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    # getting data from json request
    data = request.data
    email = data['email']
    password = data['password']

    # checking if all required fields are present
    if not email or not password:
        return Response(data={'msg': 'Email and password fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # checking if credentials are valid
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(data={'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    if not user.check_password(raw_password=password):
        return Response(data={'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # generating tokens and outputting message of successful login
    tokens = get_tokens_for_user(user=user)
    return Response(data={'msg': f'Login successful. Welcome, {user.username}!', 'tokens': tokens}, status=status.HTTP_200_OK)

