from models import Device
from flask_restful import Resource
from flask import jsonify,session,request

class DevicesByOwnerAPI(Resource):
    def get(self,owner_id):
        #get the list of devices owned by a particular user

        if not(session.get('logged_in')==True):
            return jsonify({'msg':"Session Expired. Pls login again.",'result':False})
        elif(session.get('logged_in')==True and session.get('user_id')!=str(owner_id)):
            return jsonify({'msg':"Unauthorized Access Attempt",'result':False})

        devicelist=Device.getDevicesByOwner(owner_id)
        if(isinstance(devicelist,list)):
            devicelistofdicts=[device.toDict() for device in devicelist]
            response={}
            response['devicelist']=devicelistofdicts
            response['result']=True
            return jsonify(response)
        else:
            response={}
            response['msg']=devicelist
            response['result']=False
            return jsonify(response)

    def post(self,owner_id):
        #adds a new device
        
        post_data=request.get_json()
        d=Device()
        d.setname(post_data.get('name'))
        d.setowner(owner_id)
        d.generateid()
        d.generateauthtoken()
        r=d.addDevice()
        if(isinstance(r,str)):
            response={}
            response['msg']=r
            response['result']=False
            return jsonify(response)
        else:
            response={}
            response['msg']="Device Successfully Added."
            response['result']=True
            return jsonify(response)