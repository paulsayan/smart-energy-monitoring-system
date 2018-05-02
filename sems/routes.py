from sems import app,mysql
from models import Device,User
from flask import redirect, url_for, request, render_template, jsonify, make_response, session
from flask_restful import Resource, Api
from userapi import *
from deviceapi import *
from realtimeapi import DeviceRealTimeAPI

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

api.add_resource(DevicesByOwnerAPI,'/api/devices/<int:owner_id>',endpoint='devicesbyowner')
api.add_resource(DeviceByIdAPI,'/api/device/<device_id>',endpoint='devicebyid')
api.add_resource(DeviceStateByIdAPI,'/api/device/<device_id>/state',endpoint='devicestatebyid')

api.add_resource(DeviceRealTimeAPI,'/api/device/<device_id>/realtimedata',endpoint='device_realtimedata')

