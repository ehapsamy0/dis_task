from rest_framework import serializers,fields
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Status
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(write_only=True,required=False,allow_empty_file=True)
    phone = serializers.CharField(max_length=120)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=120)
    last_name = serializers.CharField(max_length=120)
    gender = serializers.CharField(max_length=20)
    country_code = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=120,write_only=True)
    birthdate = serializers.DateField()
    # phone = PhoneNumberField()

    class Meta:
        model = User
        fields = [
            'phone',
            'email',
            "first_name",
            "last_name",
            "gender",
            "country_code",
            "phone",
            "avatar",
            "password",
            "birthdate"
        ]
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True,source="auth-token")

    class Meta:
        model = User
        fields = [
            "token",
        ]
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)



class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"