from models import Session,UserSetting,Device
from flask_restful import Resource
from flask import jsonify,session,request
import redis
from ast import literal_eval

class AnyBillAPI(Resource):
    def get(self,user_id):

        startdate=request.args.get('startdate')
        enddate=request.args.get('enddate')

        r=Session.getEnergyConsumedPerDeviceByOwner(user_id,startdate,enddate)
        response={}
        if(isinstance(r,list)):
            response['devicelist']=r
            response['totalenergyc']=self.calcTotalEnergyConsumption(r)
            response['result']=True
            return jsonify(response)
        else:
            response['msg']=r
            response['result']=False
            return jsonify(response)

    def calcTotalEnergyConsumption(self,devicelist):
        totalenergy=0.0
        for device in devicelist:
            totalenergy=totalenergy+device['energyc']
        return totalenergy


class RealtimeBillAPI(Resource):
    def __init__(self):
        self.db=redis.StrictRedis(host="localhost", port=6379, db=0)

    def calcTotalEnergyConsumption(self,devicelist):
        totalenergy=0.0
        for device in devicelist:
            totalenergy=totalenergy+device['energyc']
        return totalenergy

    def get(self,user_id):
        response=self.getBill(user_id)
        response['result']=True
        return jsonify(response)


    def getBill(self,user_id):
        
        us=UserSetting.getSetting(user_id,'lastbilldate')
        us_dict=us.toDict()
        lastbilldate=us_dict['value']

        print(lastbilldate)

        rows=Session.getEnergyConsumedPerDeviceByOwner(user_id,lastbilldate=lastbilldate)

        if(isinstance(rows,list)):
            totalenergyc_completedsessions=self.calcTotalEnergyConsumption(rows)
        else:
            totalenergyc_completedsessions=0.0

        
        devicelist=Device.getDevicesByOwner(user_id)
        if(isinstance(devicelist,list)):
            activedevicelist=[device for device in devicelist if device.getstate()==True]
            if(activedevicelist==[]):
                totalenergyc_ongoingsessions=0.0
            else:
                totalenergyc_ongoingsessions=0.0
                for device in activedevicelist:
                    dbkey="device:"+device.getid()
                    dbval=self.db.get(dbkey)
                    if(dbval!=None):
                        devicertdata=literal_eval(dbval)
                        totalenergyc_ongoingsessions+=devicertdata['energyc']
                        
                        found=False
                        for i in range(len(rows)):
                            if(rows[i]['id']==device.getid()):
                                rows[i]['rtenergyc']=devicertdata['energyc']
                                found=True
                                break
                        
                        if(found==False):
                            d={}
                            d['id']=device.getid()
                            d['name']=device.getname()
                            d['rtenergyc']=devicertdata['energyc']
                            rows.append(d)


        else:
            totalenergyc_ongoingsessions=0.0
                    
        print(rows)

        totalenergyc=totalenergyc_completedsessions+totalenergyc_ongoingsessions

        d={}
        d['totalenergyc']=totalenergyc
        d['totalenergyc_completedsessions']=totalenergyc_completedsessions
        d['totalenergyc_ongoingsessions']=totalenergyc_ongoingsessions
        d['devicelist']=rows

        return d


            


        

        

        