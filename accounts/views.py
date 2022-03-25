
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer, UserSerializerWithToken, StatusSerializer
# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password
from rest_framework import status

User = get_user_model()




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        data.pop("refresh",None)
        data.pop("access",None)
        data['auth-token'] = data['token']
        data.pop("token",None)
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer





class RegisterUser(APIView):
    serializer_class = UserSerializer
    def post(self,request):
        data = request.data
        try:

            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                gender=data['gender'],
                email=data['email'],
                phone=data['phone'],
                birthdate=data['birthdate'],
                country_code=data['country_code'],
                password=make_password(data['password'])
            )

            serializer = UserSerializer(user, many=False)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except:
            return Response({ "errors": { "first_name": [ { "error": "blank" } ], "last_name": [ { "error":"blank" } ], "country_code":[ { "error": "inclusion" } ], "phone_number":[ { "error": "blank" }, { "error": "not_a_number" }, { "error":
                                "not_exist" }, { "error": "invalid" }, { "error": "taken" }, { "error":
                                "too_short", "count": 10 }, { "error": "too_long", "count": 15 } ], "gender":[ { "error": "inclusion" } ], "birthdate": [ { "error": "blank" },
                                { "error": "in_the_future" } ], "avatar": [ { "error": "blank" }, { "error":"invalid_content_type" } ], "email": [{ "error": "taken" }, { "error":
                                "invalid" } ] } },status=status.HTTP_400_BAD_REQUEST)






class CreateStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializable = StatusSerializer

    def post(self,request):
        data = request.data
        user = request.user
        phone = data['phone']
        try:

            check_user = User.objects.get(phone=phone)
        except:
            return Response({
                'Message': "No User For This Phone"
            },status=status.HTTP_404_NOT_FOUND)

        if check_user.id == user.id:
            new_request_data = data.copy()
            new_request_data.update({'user': str(check_user.id)})
            serializer = StatusSerializer(data=new_request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response({
                'Message': "unauthorized request or bad request",
                "Errors":serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'Message': "unauthorized request or bad request"
        },status=status.HTTP_400_BAD_REQUEST)

