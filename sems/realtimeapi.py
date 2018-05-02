from models import Device
from flask_restful import Resource
from flask import jsonify,session,request
import redis
from ast import literal_eval

class DeviceRealTimeAPI(Resource):
    def __init__(self):
        self.db=redis.StrictRedis(host="localhost", port=6379, db=0)
    
    def post(self,device_id):
        post_data=request.get_json()
        device={}
        device['instpower']=post_data.get('instpower')
        dbkey="device:"+device_id
        r=self.db.set(dbkey,device)
        if(r==True):
            return jsonify({'result':True})
        else:
            return jsonify({'result':False})

    def get(self,device_id):
        dbkey="device:"+device_id
        dbval=self.db.get(dbkey)
        if(dbval==None):
            return jsonify({'result':False})

        device=literal_eval(dbval)
        device['result']=True
        return jsonify(device)

