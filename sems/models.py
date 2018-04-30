from sems import app
import string
import uuid
from random import choice,randint
from daoclass import DAOClass
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
import jwt

class Device():
	def __init__(self,owner1,name1):
		self.name=name1
		self.state=False
		self.instpower=0.0
		self.energyc=0.0
		self.owner=int(owner1)
		self.auth_token=self.generateauthtoken()
		self.id=self.generateid(owner1)

	def generateid(self,owner1):
		min_char = 8
		max_char = 8
		allchar = string.ascii_letters + string.digits
		randomstring = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
		return owner1+"_"+randomstring

	def generateauthtoken(self):
		return str(uuid.uuid4())

	def getid(self):
		return self.id

	def getname(self):
		return self.name

	def getinstpower(self):
		return self.instpower

	def getenergyc(self):
		return self.energyc

	def getowner(self):
		return self.owner

	def getstate(self):
		return self.state

	def addDevice(self):
		dao=DAOClass()
		sql="select * from devices where owner="+str(self.owner)+" and name='"+self.name+"'"
		print(sql)
		r=dao.getData(sql)
		print(r)
		if(r==[]):
			sql="insert into devices(id,name,state,owner,authtoken) values('"+self.id+"','"+self.name+"',"+str(int(self.state))+","+str(self.owner)+",'"+self.auth_token+"')"
			print(sql)
			r=dao.updateData(sql)
			return r
		else:
			return False



class User():
	
	def __init__(self):
		self.id=""
		self.name=""
		self.email=""
		self.pwd=""

	def setpwd(self,pwd1):
		self.pwd=generate_password_hash(pwd1)

	def setpwdhash(self,phash):
		self.pwd=phash
	
	def checkpwd(self,pwd1):
		return check_password_hash(self.pwd,pwd1)

	def getid(self):
		return self.id
	
	def setid(self,id1):
		self.id=id1

	def setname(self,name1):
		self.name=name1

	def setemail(self,email1):
		self.email=email1

	def getname(self):
		return self.name

	def getemail(self):
		return self.email

	@classmethod
	def rowtoDict(cls,row):
		d={}
		d['id']=row[0]
		d['name']=row[1]
		d['email']=row[2]
		d['pwd']=row[4]
		return d

	def toDict(self):
		d={}
		d['id']=self.id
		d['name']=self.name
		d['email']=self.email
		return d

	@classmethod
	def rowtoObj(cls,row):
		u=User()
		u.id=row[0]
		u.name=row[1]
		u.email=row[2]
		u.pwd=row[3]
		return u 

	@classmethod
	def getUserById(cls,id1):
		dao=DAOClass()
		sql="select * from users where id='"+id1+"'"
		print("getUserById: "+sql)
		rows=dao.getData(sql)
		if not rows:
			msg="Database Error"
			print(msg)
			return msg
		elif (rows==[]):
			msg="User Not Found"
			print(msg)
			return msg
		else:
			#r=[cls.rowtoDict(row) for row in rows]
			r=cls.rowtoObj(rows[0])
			print(r)
			return r
	
	@classmethod
	def getUserByEmail(cls,email1):
		dao=DAOClass()
		sql="select * from users where email='"+email1+"'"
		print("getUserByEmail: "+sql)
		rows=dao.getData(sql)
		if(rows==None):
			msg="Database Error"
			print(msg)
			return msg
		elif (rows==[]):
			msg="User Not Found"
			print(msg)
			return msg
		else:
			#r=[cls.rowtoDict(row) for row in rows]
			r=cls.rowtoObj(rows[0])
			print(r)
			return r
	
	
	def addUser(self):
		u=User.getUserByEmail(self.email)
		if(u=="User Not Found"):
			dao=DAOClass()
			sql="insert into users(name,email,pwd) values('"+self.name+"','"+self.email+"','"+self.pwd+"')"
			print("addUser: "+sql)
			r=dao.updateData(sql)
			if(r==True):
				u=User.getUserByEmail(self.email)
				return u
				"""
				if(isinstance(u,User)):
					return u.getid()
				else:
					return u
				"""

			else:
				return "Database Error"
		elif(u=="Database Error"):
			return "Database Error"
		else:
			msg="User Already Exists"
			print(msg)
			return msg

	def updateUserById(self):
		dao=DAOClass()
		sql="update table users set name='"+self.name+"', email='"+self.email+"', pwd='"+self.pwd+"' where id="+self.id
		print("updateUserById: "+sql)
		r=dao.updateData(sql)
		if(r==True):
			msg="User Data Updated"
			print(msg)
			return msg
		else:
			msg="Database Error"
			print(msg)
			return msg

	"""
	def encode_auth_token(self, user_id):
		try:
			payload = {
            	'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=30),
            	'iat': datetime.datetime.utcnow(),
            	'sub': user_id
        	}
			return jwt.encode(
            	payload,
            	app.config.get('SECRET_KEY'),
            	algorithm='HS256'
        	)
		except Exception as e:
			return e

	@staticmethod
	def decode_auth_token(auth_token):
		try:
			payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
			return payload['sub']
		except jwt.ExpiredSignatureError:
			return 'Signature expired. Please log in again.'
		except jwt.InvalidTokenError:
			return 'Invalid token. Please log in again.'

		
	"""


	