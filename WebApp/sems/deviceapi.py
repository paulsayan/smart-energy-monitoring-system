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


class DeviceByIdAPI(Resource):
    def get(self,device_id):
        d=Device.getDeviceById(device_id)
        if(isinstance(d,Device)):
            response=d.toDict()
            response['result']=True
            return jsonify(response)
        else:
            response={}
            response['msg']=d
            response['result']=True
            return jsonify(response)
    
    def post(self,device_id):
        post_data=request.get_json()
        d=Device.getDeviceById(device_id)
        if not(isinstance(d,Device)):
            response={}
            response['msg']=d
            response['result']=False
            return jsonify(response)

        d.setname(post_data.get('name'))

        r=d.updateDevice()
        if(isinstance(r,str)):
            response={}
            response['msg']=r
            response['result']=False
            return jsonify(response)
        else:
            response={}
            response['msg']="Device Updated Successfully."
            response['result']=True
            return jsonify(response)

    def delete(self,device_id):
        d=Device.getDeviceById(device_id)
        if not(isinstance(d,Device)):
            response={}
            response['msg']=d
            response['result']=False
            return jsonify(response)
        
        r=Device.deleteDeviceById(device_id)
        if(r==False):
            response={}
            response['msg']="Device Deletion Unsuccessful."
            response['result']=False
            return jsonify(response)
        else:
            response={}
            response['msg']="Device deleted successfully."
            response['result']=True
            return jsonify(response)

        

class DeviceStateByIdAPI(Resource):
    def get(self,device_id):
        d=Device.getDeviceById(device_id)
        if(isinstance(d,Device)):
            response={}
            response['state']=d.getstate()
            response['result']=True
            return jsonify(response)
        else:
            response={}
            response['msg']=d
            response['result']=False
            return jsonify(response)
        
    def post(self,device_id):
        post_data=request.get_json()
        d=Device.getDeviceById(device_id)
        if not(isinstance(d,Device)):
            response={}
            response['msg']=d
            response['result']=False
            return jsonify(response)

        r=Device.updateDeviceStateById(device_id,post_data.get('state'))
        if(r==False):
            response={}
            response['msg']="Device State Update Unsuccessful."
            response['result']=False
            return jsonify(response)
        else:
            response={}
            response['msg']="Device State Updated Successfully."
            response['result']=True
            return jsonify(response)