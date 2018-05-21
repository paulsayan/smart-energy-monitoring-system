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

from sems.models import Session,UserSetting,Device,Notification
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


class UpdateBillsAPI(Resource):
    def get(self):

        if(request.args.get('user')!=None):
            user_id=request.args.get('user')
        elif(request.args.get('device')!=None):
            deviceid=request.args.get('device')
            device=Device.getDeviceById(deviceid)
            user_id=device.getowner()
        else:
            return jsonify({'result':False})

        #realtimebill=RealtimeBillAPI().getBill(user_id)
        #lastbilldate=UserSetting.getSetting(user_id,'lastbilldate')

        lastbilldate_updated=UserSetting.updateLastBillDate(user_id)
        if(lastbilldate_updated==True):
            #session energyc split
            #realtime bill -> stored bill
            pass

        realtimebill=RealtimeBillAPI().getBill(user_id)
        energyc_now=realtimebill['totalenergyc']
        energyc_quota=float(UserSetting.getSetting(user_id,'energyc_quota').toDict()['value'])

        billingcycle=UserSetting.getSetting(user_id,'billingcycle').toDict()['value']
        billstartdate,billenddate=UserSetting.getBillingPeriodDates(user_id,billingcycle)

        notification_generated=False
        if(energyc_now>energyc_quota):
            alreadynotified=False
            billingcycle=UserSetting.getSetting(user_id,'billingcycle').toDict()['value']
            billstartdate,billenddate=UserSetting.getBillingPeriodDates(user_id,billingcycle)
            user_notifications=Notification.getNotificationsByUserIdAndDates(user_id,billstartdate,billenddate)
            if(isinstance(user_notifications,list)):
                user_notifications_d=[n.toDict() for n in user_notifications]
                for n in user_notifications_d:
                    if(n['type']=='ENERGYC_QUOTA_EXCEEDED'):
                        alreadynotified=True
            
            if(alreadynotified==False):
                new_notification=Notification()
                new_notification.setuserid(user_id)
                new_notification.settype('ENERGYC_QUOTA_EXCEEDED')
                n_msg="Your devices have exceeded the energy consumption quota for the billing period \
                "+billstartdate+" to "+billenddate+"."
                new_notification.setmsg(n_msg)
                notification_generated=new_notification.addNotification()


        response={}
        response['lastbilldate_updated']=lastbilldate_updated
        response['notification_generated']=notification_generated
        response['billstartdate']=billstartdate
        response['billenddate']=billenddate
        response['energyc_quota']=energyc_quota
        response['result']=True
        return jsonify(response)


        

        