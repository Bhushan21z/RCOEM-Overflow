from os import stat
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests

from .handleDB import *
from .serializers import *


@api_view(['POST'])
def register(request):
	
	return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
	
	return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def view_all_questions(request):
	
	data=get_all_questions()
	return Response(data)


@api_view(['POST'])
def view_unanswered_questions(request):
	
	data=get_unanswered_questions()
	return Response(data)


@api_view(['POST'])
def add_question(request):
	"""
	{
		"author": "demouser4",
		"email": "demouser4@gmail.com",
		"password":"password",
		"question":"How to be a full stack developer?"
	}
 	"""
	serializer = AddQuestionSerializer(data=request.data)

	if serializer.is_valid():
		data = serializer.data
		question=data['question']
		author=data['author']
		password=data['password']
		email=data['email']
		check=checkUser(author,password,email)
		if(check==True):
			add_question_db(question,author)
			return Response("Question added successfully")
		else:
			return Response("INVALID USER DATA")
	else:
    		return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['POST'])
def add_answer(request):
	"""
	{
		"author": "demouser4",
		"email": "demouser10@gmail.com",
		"password":"password",
		"question":"How to be a full stack developer?",
		"answer":"Follow angela yu web development course on udemy."
	}
 	"""
	serializer = AddAnswerSerializer(data=request.data)

	if serializer.is_valid():
		data = serializer.data
		question=data['question']
		author=data['author']
		password=data['password']
		email=data['email']
		answer=data['answer']
		check=checkUser(author,password,email)
		if(check==True):
			add_answer_db(question,author,answer)
			return Response("Answer added successfully")
		else:
			return Response("INVALID USER DATA")
	else:
    		return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)