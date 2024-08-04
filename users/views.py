from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CustomUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(request.data)
            return Response(CustomUserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class HomeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                users = User.objects.all()
                serializer = CustomUserSerializer(users, many=True)
                return Response({
                    "message": "List of all users",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            serializer = CustomUserSerializer(user)
            return Response({
                        "message": f"Welcome {user.first_name} to the HomePage",
                        "data": serializer.data
                    },  status=status.HTTP_200_OK)

        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user_id=kwargs.get('id')
        if request.user.is_staff:
            user = get_object_or_404(User, id=user_id)
            serializer = CustomUserSerializer(user)
            return Response({
                "message": f"Detail of ID: {user.id}",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
    def post(self, request,*args, **kwargs):
        if request.user.is_staff:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "msg": "User created Successfully",
                    "data":serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    def put(self, request, *args, **kwargs):
        if request.user.is_staff:
            user_id = kwargs.get('id')   
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({
                    'error': 'User Not Found'},
                     status=status.HTTP_404_NOT_FOUND)
            serializer = CustomUserSerializer(user,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "User updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs ):
        if request.user.is_staff:
            user_id = kwargs.get('id')
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User Not Exist"}, status=status.HTTP_404_NOT_FOUND)
            serializer = CustomUserSerializer(user,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                        "message": "User partially updated successfully",
                        "data": serializer.data
                    }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        if request.user.is_staff:
            user_id = kwargs.get('id')  
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


