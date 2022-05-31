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
