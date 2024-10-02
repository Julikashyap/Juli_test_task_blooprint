from rest_framework import serializers
from tes_app.models import User
from .models import Category, Product, Stock

class RegisterSerialization(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    address = serializers.CharField(required=True)
    pin_code = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class LoginSerialization(serializers.Serializer):
    email = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

class LogOutSerializer(serializers.Serializer):
    pass

class UpdateProfileImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=False)

class UserSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'name', 'address', 'pin_code', 'city', 'country', 'image']

class CreateUserSerial(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    address = serializers.CharField(required=True)
    pin_code = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    country = serializers.CharField(required=True)

class ChangePasswordSerial(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class Forgetpasswordserial(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100)
    redirecturl = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["email", "redirecturl"]

class ResetPasswordSeriel(serializers.Serializer):
    token=serializers.CharField(max_length=500)
    new_password = serializers.CharField(max_length=30, min_length=4)
    confirm_password = serializers.CharField(max_length=20, min_length=4)

class AssignRoleSerialization(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = Stock
        fields = '__all__'