import json
import firebase_admin
from firebase_admin import credentials, firestore
from grpc import Status
cred = credentials.Certificate('credentials.json')

firebase_admin.initialize_app(cred)
db = firestore.client()


def get_all_questions():
    index=db.collection('index').document('index').get()
    getindex=index.to_dict()
    index=getindex['index']
    returndata=[]
    
    for i in range(index):
          returnmap={}
          question_no='question'+str(i+1)
          data=db.collection('questions').document(question_no).get()
          data=data.to_dict()
          answerlen=len(data['answers'])
          if(answerlen>0):
                returnmap['author']=data['author']
                returnmap['no_of_answers']=answerlen
                returnmap['views']=data['views']
                returnmap['upvotes']=data['upvotes']
                returnmap['question']=data['question']
                returndata.append(returnmap)
    
    return returndata
  
def get_unanswered_questions():
    index=db.collection('index').document('index').get()
    getindex=index.to_dict()
    index=getindex['index']
    returndata=[]
    
    for i in range(index):
          returnmap={}
          question_no='question'+str(i+1)
          data=db.collection('questions').document(question_no).get()
          data=data.to_dict()
          answerlen=len(data['answers'])
          if(answerlen==0):
                returnmap['author']=data['author']
                returnmap['question']=data['question']
                returndata.append(returnmap)
    
    return returndata

def checkUser(author,password,email):
      return True

def add_question_db(question,author):
      data={
            'question':question,
            'answers':[],
            'upvotes':0,
            'views':0,
            'author':author,
      }
      index=db.collection('index').document('index').get()
      getindex=index.to_dict()
      index=getindex['index']+1
      db.collection('index').document('index').update({'index':index})
      question_no='question'+str(index)
      db.collection('questions').document(question_no).set(data)
      

def add_answer_db(question,author,answer):
      qdata=db.collection('questions').where("question", "==", question).get()
      for doc in qdata:
            key = doc.id
            break
      qdata=qdata[0].to_dict()
      answer_array=qdata['answers']
      
      data={
            'answer':answer,
            'author':author,
            'upvotes':0,
            'comments':[],
      }
      answer_array.append(data)
      db.collection('questions').document(key).update({"answers":answer_array})
