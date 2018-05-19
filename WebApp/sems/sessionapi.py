from sems.models import Session
from flask_restful import Resource
from flask import jsonify,session,request

class SessionsByDeviceAPI(Resource):
    def get(self,device_id):

        sessionlist=Session.getSessionsByDevice(device_id)
        if(isinstance(sessionlist,list)):
            sessionlistofdicts=[session.toDict() for session in sessionlist]
            response={}
            response['sessionlist']=sessionlistofdicts
            response['result']=True
            return jsonify(response)
        else:
            response={}
            response['msg']=sessionlist
            response['result']=False
            return jsonify(response)

    def post(self,device_id):

        s=Session(device_id)
        session_id=s.addSession()
        if(isinstance(session_id,int)):
            response={}
            response['result']=True
            response['sid']=session_id
            return jsonify(response)
        else:
            response={}
            response['result']=False
            return jsonify(response)

    
    def delete(self,device_id):
        s=Session.getSessionsByDevice(device_id)
        if not(isinstance(s,list)):
            response={}
            response['msg']=s
            response['result']=False
            return jsonify(response)

        r=Session.deleteSessionsByDevice(device_id)
        if(r==False):
            response={}
            response['msg']="Sessions Deletion Unsuccessful."
            response['result']=False
            return jsonify(response)
        else:
            response={}
            response['msg']="Sessions deleted successfully."
            response['result']=True
            return jsonify(response)


class SessionByIdAPI(Resource):
    def get(self,session_id):
        s=Session.getSessionById(session_id)
        if(isinstance(s,Session)):
            response=s.toDict()
            response['result']=True
            return jsonify(response)
        else:
            response={}
            response['msg']=s
            response['result']=True
            return jsonify(response)

    def post(self,session_id):

        post_data=request.get_json()
        s=Session()
        s.setid(session_id)
        s.setenergyconsumed(post_data.get('energyc'))
        r=s.updateSession()
        if(r==False):
            response={}
            response['result']=False
            return jsonify(response)
        else:
            response={}
            response['result']=True
            return jsonify(response)


    def delete(self,session_id):

        s=Session.getSessionById(session_id)
        if not(isinstance(s,Session)):
            response={}
            response['msg']=s
            response['result']=False
            return jsonify(response)

        r=Session.deleteSessionById(session_id)
        if(r==False):
            response={}
            response['msg']="Session Deletion Unsuccessful."
            response['result']=False
            return jsonify(response)
        else:
            response={}
            response['msg']="Session deleted successfully."
            response['result']=True
            return jsonify(response)

