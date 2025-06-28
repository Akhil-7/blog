from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, LoginSerializer
# Create your views here.

class RegistrationView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    {
                        "data": serializer.errors,
                        "message": "Error occured",
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(
                {
                    "data":{},
                    "message":" Account created"
                }, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    "data":{e},
                    "message":"Error occured"
                }, status=status.HTTP_400_BAD_REQUEST
            )

class LoginView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response(
                    {
                        "data": serializer.errors,
                        "message": "Invalid credentials"
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            token_request = serializer.get_jwt_token(serializer.validated_data)
            return Response(
                token_request, status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response(
                {
                    "data":{e},
                    "message":"Error occured"
                }, status=status.HTTP_400_BAD_REQUEST
            )
