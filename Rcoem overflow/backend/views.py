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
