from os import stat
from django.http import HttpResponse, JsonResponse

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import requests

from .handleDB import *
from .serializers import *

###############################################################################

@api_view(['POST'])
def register(request):
    
    """
    {
        "name": "Demo User 2",
        "user_name": "demouser2",
        "email": "demouser2@gmail.com",
        "mobile": 2222222222,
		"password": "pswd_2"
    }
    """
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        
        data = serializer.data
        
        user_data = {
            'name': data['name'],
            'user_name': data['user_name'],
            'email': data['email'],
            'mobile': data['mobile'],
            'password': data['password']
        }

        email=data['email']

        if (check_email_exist(email) != 0):
            print("EMAIL ALREADY EXIST")
            return Response("EMAIL ALREADY EXIST", status=status.HTTP_400_BAD_REQUEST)
        else:
            print("NEW USER FOUND")
            create_user(email,user_data)
            return Response("REGISTERED SUCCESSFULLY", status=status.HTTP_201_CREATED)

    else:
        return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################


@api_view(['POST'])
def login(request):

    """
    {
        "user_name": "demouser2",
        "email": "demouser2@gmail.com",
		"password": "pswd_2"
    }
    """
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data

        user_name = data['user_name']
        email = data['email']
        password = data['password']
        
        print(user_name)
        print(email)
        print(password)
        
        if(user_name=="" and email==""):
            return Response("Invalid Credentials !! \nPlease Try Again", status=status.HTTP_401_UNAUTHORIZED)
        
        if(email!=""):
            
            if(check_email_exist(email)==1):
                
                if(verify_login_by_email(email,password)==1):
                    print("LOGGED IN SUCCESFULLY")
                    return Response("LOGGED IN SUCCESSFULLY", status=status.HTTP_200_OK)
                else:
                    print("INVALID PASSWORD")
                    return Response("Invalid Password !! \nPlease Try Again", status=status.HTTP_401_UNAUTHORIZED)
                
            elif(check_email_exist(email) == -1):
                print("Cant verify email (-1)")
                return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)
            
            else:
                print("EMAIL DOES NOT EXIST")
                return Response("EMAIL DOES NOT EXIST", status=status.HTTP_404_NOT_FOUND)
        
        if(user_name!=""):
            
            if(check_username_exist(user_name)==1):
                
                if(verify_login_by_username(user_name,password)==1):
                    print("LOGGED IN SUCCESFULLY")
                    return Response("LOGGED IN SUCCESSFULLY", status=status.HTTP_200_OK)
                else:
                    print("INVALID PASSWORD")
                    return Response("Invalid Password !! \nPlease Try Again", status=status.HTTP_401_UNAUTHORIZED)
            
            elif(check_username_exist(user_name) == -1):
                
                print("Cant verify Username (-1)")
                return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)
            
            else:
                print("USER NAME DOES NOT EXIST")
                return Response("USERNAME DOES NOT EXIST", status=status.HTTP_404_NOT_FOUND)


    else:
        return Response("INVALID SERIALIZED DATA", status=status.HTTP_400_BAD_REQUEST)


###############################################################################


@api_view(['POST'])
def register_contributor(request):
    """
    {
        "email": "demouser1@gmail.com",
        "college": "RCOEM",
        "year": 2,
        "branch" : "CSE",
        "profile_url" : "https://www.google.com",
        "points": 0,
        "skills": "C++,C,JAVA,DJANGO"
    }
    """
    serializer = AuthenticateSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.data
        
        email=data['email']
        college=data['college']
        year=data['year']
        branch=data['branch']
        profile_url=data['profile_url']
        skills_str=data['skills']
        points=0
        skills=covert_string_to_skills_list(skills_str)       
        
        user_data = {
            'college': college,
            'year': year,
            'branch': branch,
            'profile_url': profile_url,
            'skills': skills,
            'points': points            
        }
        
        if (check_email_exist(email) == 0):
            print("NO USER FOUND")
            return Response("NO USER FOUND", status=status.HTTP_404_NOT_FOUND)
        
        elif (check_email_exist(email) == -1):
            print("ERROR")
            return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)
        
        elif (check_email_exist(email) == 1):
            
            print("USER FOUND")
            
            if(add_authentication_user_data(email,user_data)==1):
                return Response("PROFILE UPDATED", status=status.HTTP_200_OK) 
            else:
                print("ERROR IN UPDATING DATA")
                return Response("PLEASE TRY AGAIN", status=status.HTTP_403_FORBIDDEN)
            
    return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################


@api_view(['POST'])
def view_all_questions(request):

    data = get_all_questions()
    return Response(data)

###############################################################################

@api_view(['POST'])
def view_trending_questions(request):

    data = get_trending_questions()
    return Response(data)

###############################################################################

@api_view(['POST'])
def view_unanswered_questions(request):

    data = get_unanswered_questions()
    return Response(data)

###############################################################################

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
        question = data['question']
        author = data['author']
        password = data['password']
        email = data['email']
        check = checkUser(author, password, email)
        if(check == True):
            add_question_db(question, author)
            return Response("Question added successfully")
        else:
            return Response("INVALID USER DATA")
    else:
        return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################

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
        question = data['question']
        author = data['author']
        password = data['password']
        email = data['email']
        answer = data['answer']
        check = checkUser(author, password, email)
        if(check == True):
            add_answer_db(question, author, answer)
            return Response("Answer added successfully")
        else:
            return Response("INVALID USER DATA")
    else:
        return Response("INVALID DATA", status=status.HTTP_400_BAD_REQUEST)

###############################################################################

@api_view(['POST'])
def view_specific_question(request):
    """
        {
                "question":"How to start with competetive programming?"
        }
        """
    serializer = ViewSpecificQuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.data['question']
    data = get_specific_question(question)
    return Response(data)

###############################################################################


###############################################################################

