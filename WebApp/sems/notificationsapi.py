from sems.models import Notification
from flask_restful import Resource
from flask import jsonify,session,request

class NotificationsAPI(Resource):
    def get(self,user_id):
        response={}
        user_notifications=Notification.getNotificationsByUser(user_id)
        if(isinstance(user_notifications,list)):
            user_notifications_d=[n.toDict() for n in user_notifications]
            response['notifications']=user_notifications_d
            response['result']=True
        else:
            response['msg']=user_notifications
            response['result']=False
        return jsonify(response)

    def put(self,nid):
        response={}
        r=Notification.readNotification(nid)
        response['result']=r
        return jsonify(response)