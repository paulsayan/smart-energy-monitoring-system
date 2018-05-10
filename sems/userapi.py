from models import User,UserSetting
from flask_restful import Resource
from flask import jsonify,session,request

class UserRegistrationAPI(Resource):
	def post(self):
		post_data=request.get_json()
		u=User()
		u.setname(post_data.get('name'))
		u.setemail(post_data.get('email'))
		u.setpwd(post_data.get('pwd'))
		u=u.addUser()
		d={}
		status=""
		if(isinstance(u,User)):
			status="success"
			d=u.toDict()
		else:
			status=u
		
		d['result']=status
		return jsonify(d)

class UserLoginAPI(Resource):
	def post(self):
		post_data=request.get_json()
		u=User.getUserByEmail(post_data.get('email'))
		d={}
		status=""
		msg=""
		if(isinstance(u,User)):
			if(u.checkpwd(post_data.get('pwd'))):
				status=True
				session['logged_in']=True
				session['user_id']=str(u.getid())
				d=u.toDict()

			else:
				msg="Invalid Credentials."
				status=False
		else:
			msg=u
			status=False
		
		d['msg']=msg
		d['result']=status
		return jsonify(d)
	
class UserLogoutAPI(Resource):
	def get(self):
		session.pop('logged_in', None)
		session.pop('user_id', None)
		return jsonify({'result': 'success'})
	def post(self):
		session.pop('logged_in', None)
		session.pop('user_id', None)
		return jsonify({'result': 'success'})

class UserStatusAPI(Resource):
    def get(self):
        if session.get('logged_in'):
            if session['logged_in']:
                return jsonify({'status': True})
        else:
            return jsonify({'status': False})


class UserSettingsAPI(Resource):
	def get(self,user_id):

		response={}
		uslist=UserSetting.getAllSettings(user_id)
		if not(isinstance(uslist,list)):
			response['result']=False
			response['msg']="Invalid User Id"
			return jsonify(response)

		uslist_d=[us.toDict() for us in uslist]
		response['settings']=uslist_d
		response['result']=True
		return jsonify(response)

		