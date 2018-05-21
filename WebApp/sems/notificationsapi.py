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