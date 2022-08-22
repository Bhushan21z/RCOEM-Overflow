from unittest.util import _MAX_LENGTH
from rest_framework import serializers

###############################################################################

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 100)
    email = serializers.EmailField(max_length = 100)
    password = serializers.CharField(max_length=100)

###############################################################################

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100)
    password = serializers.CharField(max_length=100)

###############################################################################

class CityCountSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100)
    
class CityIncrSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 100)