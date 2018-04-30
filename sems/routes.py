from sems import app,mysql
from models import Device,User
from flask import redirect, url_for, request, render_template, jsonify, make_response, session
from flask_restful import Resource, Api

api=Api(app)

@app.route('/')
@app.route('/index')
def index():
    #return redirect(url_for('static',filename='index.html'))
	return "Server OK"


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
		return jsonify({'result': 'success'})
	def post(self):
		session.pop('logged_in', None)
		return jsonify({'result': 'success'})


api.add_resource(UserRegistrationAPI,'/api/user/register',endpoint='user_register')
api.add_resource(UserLoginAPI,'/api/user/login',endpoint='user_login')
api.add_resource(UserLogoutAPI,'/api/user/logout',endpoint='user_logout')



