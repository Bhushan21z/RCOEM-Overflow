import json
import firebase_admin
from firebase_admin import credentials, firestore
from grpc import Status
cred = credentials.Certificate('credentials.json')

firebase_admin.initialize_app(cred)
db = firestore.client()

###############################################################################

def check_email_exist(email):
    try:
        # print("no error")
        user_id = email.split("@")[0]
        user = db.collection('users').document(user_id).get()
        # print(user)
        if(user.exists):
            return 1
        else:
            return 0
    except:
        # print("error")
        return -1
        
# print(check_email_exist("firstuser@gmail.com"))

###############################################################################

def create_user(email,data):
    
    try:
        user_id = email.split("@")[0]
        db.collection('users').document(user_id).set(data)
        
        stats=db.collection('stats').document('counts')
        stats.update({"total_users": firestore.Increment(1)})
        
        print("New User Created")
    except:
        print("ERROR IN CREATE_USER")


# create_user("demouser6@gmail.com",{
#             'name': 'Demo User6',
#             'email': 'demouser6@gmail.com',
#             'password': 'pswd6',
#             'curr_city': 0,
#             'india_game_status': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#         })

###############################################################################

def get_user_data(email):
    try:
        users = db.collection("users").where('email', '==', email).get()

        if len(users) > 0:
            userdata = users[0].to_dict()
            return userdata
        else:
            userdata = {}
            return userdata
    except:
        print("ERROR IN GET_USER_DATA")
        return -1


###############################################################################

def login_by_email(email,password):
    try:
        user_id = email.split("@")[0]
        # print("1")
        user = db.collection('users').document(user_id).get()
        userdata = user.to_dict()   
        # print("2")
        # print(userdata)         
        
        if(password == userdata['password']):
            print("Valid User")
            return 1
        else:
            print("Wrong Password")
            return 0
    except:
        print("ERROR IN LOGIN")
        return -1
    
###############################################################################

def city_count(email):
    user_id = email.split("@")[0]
    user = db.collection('users').document(user_id).get()
    userdata=user.to_dict()  
    print(userdata['curr_city'])
    print("---------------------------------")
    return userdata['curr_city']

def city_incre(email):
    user_id = email.split("@")[0]
    db.collection('users').document(user_id).update({"curr_city": firestore.Increment(1)})
    user = db.collection('users').document(user_id).get()
    userdata=user.to_dict() 
    print(userdata['curr_city'])
    print("---------------------------------")