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

from sems import app,mysql#,daoclass,models,userapi,deviceapi,realtimeapi,sessionapi,billsapi,notificationsapi
from sems.models import Device,User
#from sems.models import Device,User
from flask import redirect, url_for, request, render_template, jsonify, make_response, session
from flask_restful import Resource, Api

from sems.userapi import UserLoginAPI,UserLogoutAPI,UserRegistrationAPI,UserStatusAPI,UserSettingsAPI
from sems.deviceapi import DeviceByIdAPI,DevicesByOwnerAPI,DeviceStateByIdAPI
from sems.realtimeapi import DeviceRealTimeAPI,DevicesRealTimeAPI
from sems.sessionapi import SessionByIdAPI,SessionsByDeviceAPI
from sems.billsapi import AnyBillAPI,RealtimeBillAPI,UpdateBillsAPI
from sems.notificationsapi import NotificationsAPI

api=Api(app)

@app.route('/')
@app.route('/index')
def index():
    #return redirect(url_for('static',filename='index.html'))
	#return "Server OK"
	return app.send_static_file('index.html')


api.add_resource(UserRegistrationAPI,'/api/user/register',endpoint='user_register')
api.add_resource(UserLoginAPI,'/api/user/login',endpoint='user_login')
api.add_resource(UserLogoutAPI,'/api/user/logout',endpoint='user_logout')
api.add_resource(UserStatusAPI,'/api/user/status',endpoint='user_status')

api.add_resource(UserSettingsAPI,'/api/user/<int:user_id>/settings',endpoint='user_settings')

api.add_resource(DevicesByOwnerAPI,'/api/devices/<int:owner_id>',endpoint='devicesbyowner')
api.add_resource(DeviceByIdAPI,'/api/device/<device_id>',endpoint='devicebyid')
api.add_resource(DeviceStateByIdAPI,'/api/device/<device_id>/state',endpoint='devicestatebyid')

api.add_resource(DeviceRealTimeAPI,'/api/device/<device_id>/realtimedata',endpoint='device_realtimedata')
api.add_resource(DevicesRealTimeAPI,'/api/devices/<int:owner_id>/realtimedata',endpoint='devices_realtimedata')

api.add_resource(SessionsByDeviceAPI,'/api/sessions/<device_id>',endpoint='sessionsbydevice')
api.add_resource(SessionByIdAPI,'/api/session/<session_id>',endpoint='sessionbyid')

api.add_resource(AnyBillAPI,'/api/anybill/<int:user_id>',endpoint='anybill')
api.add_resource(RealtimeBillAPI,'/api/realtimebill/<int:user_id>',endpoint='realtimebill')
api.add_resource(UpdateBillsAPI,'/api/updatebills',endpoint='updatebills')

api.add_resource(NotificationsAPI,'/api/notifications/<int:user_id>',endpoint='notifications')

"""
@app.route('/api/sessions/<device_id>/')
def sessionsapi(device_id):
	return redirect('/api/sessions/'+device_id,301)

@app.route('/api/session/<session_id>/')
def sessionapi(session_id):
	return redirect('/api/session/'+session_id,301)
"""

