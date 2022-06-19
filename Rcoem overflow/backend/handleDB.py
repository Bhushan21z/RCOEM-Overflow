import json
import firebase_admin
from firebase_admin import credentials, firestore
from grpc import Status
cred = credentials.Certificate('credentials.json')

firebase_admin.initialize_app(cred)
db = firestore.client()

###############################################################################

def get_all_questions():
      index = db.collection('index').document('index').get()
      getindex = index.to_dict()
      index = getindex['index']
      returndata = []

      for i in range(index):
            returnmap = {}
            question_no = 'question'+str(i+1)
            data = db.collection('questions').document(question_no).get()
            data = data.to_dict()
            answerlen = len(data['answers'])
            if(answerlen > 0):
                  returnmap['author'] = data['author']
                  returnmap['no_of_answers'] = answerlen
                  returnmap['views'] = data['views']
                  returnmap['upvotes'] = data['upvotes']
                  returnmap['question'] = data['question']
                  returndata.append(returnmap)

      return returndata

###############################################################################

def get_unanswered_questions():
      index = db.collection('index').document('index').get()
      getindex = index.to_dict()
      index = getindex['index']
      returndata = []

      for i in range(index):
            returnmap = {}
            question_no = 'question'+str(i+1)
            data = db.collection('questions').document(question_no).get()
            data = data.to_dict()
            answerlen = len(data['answers'])
            if(answerlen == 0):
                  returnmap['author'] = data['author']
                  returnmap['question'] = data['question']
                  returndata.append(returnmap)

      return returndata

###############################################################################

def checkUser(author, password, email):
      return True

###############################################################################

def add_question_db(question, author):
      data = {
            'question': question,
            'answers': [],
            'upvotes': 0,
            'views': 0,
            'author': author,
      }
      index = db.collection('index').document('index').get()
      getindex = index.to_dict()
      index = getindex['index']+1
      db.collection('index').document('index').update({'index': index})
      question_no = 'question'+str(index)
      db.collection('questions').document(question_no).set(data)

###############################################################################

def add_answer_db(question, author, answer):
      qdata = db.collection('questions').where("question", "==", question).get()
      for doc in qdata:
            key = doc.id
            break
      qdata = qdata[0].to_dict()
      answer_array = qdata['answers']

      data = {
            'answer': answer,
            'author': author,
            'upvotes': 0,
            'comments': [],
      }
      answer_array.append(data)
      db.collection('questions').document(key).update({"answers": answer_array})

###############################################################################

def get_specific_question(question):
      qdata = db.collection('questions').where("question", "==", question).get()
      qdata = qdata[0].to_dict()
      data = {
            'question': qdata['question'],
            'views': qdata['views'],
            'upvotes': qdata['upvotes'],
            'author': qdata['author'],
            'answers': qdata['answers']
      }
      return data

###############################################################################

def get_trending_questions():
      index = db.collection('index').document('index').get()
      getindex = index.to_dict()
      index = getindex['index']
      returndata = []
      dic = {}
      for i in range(index):
            question_no = 'question'+str(i+1)
            data = db.collection('questions').document(question_no).get()
            data = data.to_dict()
            answerlen = len(data['answers'])
            if(answerlen > 0):
                  dic[(i+1)] = data['views']

      sorted_dict = {}
      sorted_keys = sorted(dic, key=dic.get)
      sorted_keys.reverse()

      for w in sorted_keys:
            sorted_dict[w] = dic[w]
            returnmap = {}
            question_no = 'question'+str(w)
            data = db.collection('questions').document(question_no).get()
            data = data.to_dict()
            returnmap['author'] = data['author']
            returnmap['no_of_answers'] = answerlen
            returnmap['views'] = data['views']
            returnmap['upvotes'] = data['upvotes']
            returnmap['question'] = data['question']
            returndata.append(returnmap)
      return returndata

###############################################################################

def check_email_exist(email):
      
      try:
            user_id = email.split("@")[0]
            user = db.collection('users').document(user_id).get()
            if(user.exists):
                  return 1
            else:
                  return 0
            
      except:
            print("ERROR IN CHECK_EMAIL_EXIST")
            return -1
      
###############################################################################

def check_username_exist(user_name):
	try:
		user = db.collection("users").where('user_name', '==', user_name).get()
		if(len(user)>0):
			return 1
		else:
			return 0
	except:
		print("ERROR IN CHECK_USERNAME_EXIST")
		return -1

###############################################################################

def create_user(email,data):
      
      try:
            user_id = email.split("@")[0]
            db.collection('users').document(user_id).set(data)
            return 1
      except:
            print("ERROR IN CREATE_USER")
            return -1

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

def verify_login_by_username(user_name,password):
      try:
            user = db.collection("users").where('user_name', u'==', user_name).get()
            userdata=user[0].to_dict()
            
            if(password==userdata['password']):
                  return 1
            else:
                  return 0
      except:
            print("ERROR IN VERIFY_LOGIN_BY_USERNAME")
            return -1

###############################################################################

def verify_login_by_email(email,password):
      try:
            user_id = email.split("@")[0]
            # print("1")
            user = db.collection('users').document(user_id).get()
            userdata=user.to_dict()   
            # print("2")
            print(userdata)         
            
            if(password == userdata['password']):
                  return 1
            else:
                  return 0
      except:
            print("ERROR IN VERIFY_LOGIN_BY_EMAIL")
            return -1
      
###############################################################################

def add_authentication_user_data(email,user_data):
      try:
            user_id = email.split("@")[0]
            db.collection('users').document(user_id).update(user_data)
            return 1
      except:
            return 0
###############################################################################

def covert_string_to_skills_list(skills_str):
      
      skills=[]
      var=""
      
      for c in skills_str:
            if(c==','):
                  skills.append(var)
                  var=""
            else:
                  var+=c                  
      skills.append(var)
      
      print(skills)
      return skills

###############################################################################
###############################################################################