from django.shortcuts import render
import json
from re import sub
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .handleDB import *
from .serializers import *


###############################################################################


@api_view(['POST'])
def register(request):
    """
    {
        "name": "Demo User 1",
        "email": "demouser1@gmail.com",
        "password": "pswd_1"
    }
    """
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        data = serializer.data

        user_data = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password'],
            'curr_city': 0,
            'india_game_status': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        }

        email = data['email']

        if (check_email_exist(email) == 1):
            print("EMAIL ALREADY EXIST")
            return Response("EMAIL ALREADY EXIST", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        elif((check_email_exist(email) == 0)):
            create_user(email, user_data)
            return Response("REGISTERED SUCCESSFULLY", status=status.HTTP_201_CREATED)
        
        else:
            print("ERROR IN REGISTERING, TRY AGAIN")
            return Response("ERROR IN REGISTERING, TRY AGAIN", status=status.HTTP_403_FORBIDDEN)

    else:
        return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################


@api_view(['POST'])
def login(request):
    
    """
    {
        "email": "demouser1@gmail.com",
        "password": "pswd_1"
    }
    """
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data
        
        email = data['email']
        password = data['password']

        # print(email)
        # print(password)
        
        if (check_email_exist(email) == 0):
            print("EMAIL DOES NOT EXIST")
            return Response("EMAIL DOES NOT EXIST", status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if (check_email_exist(email) != 1):
            print("ERROR IN REGISTERING, TRY AGAIN")
            return Response("ERROR IN REGISTERING, TRY AGAIN", status=status.HTTP_403_FORBIDDEN)
        
        if(login_by_email(email, password) == 1):
                return Response("VALID USER", status=status.HTTP_200_OK)
            
        elif(login_by_email(email, password) == 0):
            return Response("Invalid Password !! \nPlease Try Again", status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)
        
    else:
        return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)


###############################################################################

@api_view(['POST'])
def city_api(request):
    """
    {
        "email": "demouser1@gmail.com"
    }
    """
    serializer = CityCountSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.data
        email=data['email']
        count=city_count(email)
        data_return={"city":count}
        return Response(data_return)
    else:
        return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def city_increment(request):
    """
    {
        "email": "demouser1@gmail.com"
    }
    """
    serializer = CityIncrSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.data
        email=data['email']
        city_incre(email)
        return Response("City Incremented")
    else:
        return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)