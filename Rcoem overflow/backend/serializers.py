from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserSerializer(serializers.Serializer):
	name = serializers.CharField(max_length = 100)
	email = serializers.EmailField()
	college = serializers.CharField(max_length = 100)
	key = serializers.CharField(max_length=100)
	mobile = serializers.IntegerField()

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	college = serializers.CharField(max_length = 100)
	key = serializers.CharField(max_length=100)
 
class AddQuestionSerializer(serializers.Serializer):
    author= serializers.CharField(max_length=100)
    email= serializers.EmailField()
    password= serializers.CharField(max_length=100)
    question= serializers.CharField(max_length=1000)
    
class AddAnswerSerializer(serializers.Serializer):
    author= serializers.CharField(max_length=100)
    email= serializers.EmailField()
    password= serializers.CharField(max_length=100)
    question= serializers.CharField(max_length=100000000)
    answer= serializers.CharField(max_length=10000000000)

class ViewSpecificQuestionSerializer(serializers.Serializer):
    question= serializers.CharField(max_length=100000000)