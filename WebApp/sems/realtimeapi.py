"""

    Smart Energy Monitoring System
    Copyright (C) 2018 - Sayan Paul

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

from sems.models import Device
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
        device['energyc']=post_data.get('energyc')
        device['sid']=post_data.get('sid')

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

class DevicesRealTimeAPI(Resource):
    def __init__(self):
        self.db=redis.StrictRedis(host="localhost", port=6379, db=0)
    
    def get(self,owner_id):

        devicelist=Device.getDevicesByOwner(owner_id)
        if(isinstance(devicelist,str)):
            response={}
            response['msg']=devicelist
            response['result']=False
            return jsonify(response)

        deviceidlist=[device.getid() for device in devicelist if device.getstate()==True]
        if(deviceidlist==[]):
            response={}
            response['msg']="No Devices with ongoing Sessions found."
            response['result']=False
            return jsonify(response)

        devicedatalist={}
        for deviceid in deviceidlist:
            dbkey="device:"+deviceid
            dbval=self.db.get(dbkey)
            if(dbval!=None):
                devicedatalist[deviceid]=literal_eval(dbval)
        
        response={}
        response['devicedatalist']=devicedatalist
        response['result']=True
        return jsonify(response)

