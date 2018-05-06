from models import Session
from flask_restful import Resource
from flask import jsonify,session,request

class AnyBillAPI(Resource):
    def get(self,owner_id):

        startdate=request.args.get('startdate')
        enddate=request.args.get('enddate')

        r=Session.getEnergyConsumedPerDeviceByOwner(owner_id,startdate,enddate)
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