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

from sems import app
import string
import uuid
from random import choice,randint
from sems.daoclass import DAOClass
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
import jwt

class Device():
	
	def __init__(self):
		self.name=""
		self.state=False
		self.owner=0
		self.auth_token=""
		self.id=""

	"""
	def __init__(self,owner1,name1):
		self.name=name1
		self.state=False
		self.owner=int(owner1)
		self.auth_token=self.generateauthtoken()
		self.id=self.generateid(owner1)
	"""

	#def generateid(self,owner1):
	def generateid(self):
		min_char = 8
		max_char = 8
		allchar = string.ascii_letters + string.digits
		randomstring = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
		#return owner1+"_"+randomstring
		self.id=str(self.owner)+"_"+randomstring

	def generateauthtoken(self):
		#return str(uuid.uuid4())
		self.auth_token=str(uuid.uuid4())

	def getid(self):
		return self.id

	def getname(self):
		return self.name

	def getowner(self):
		return self.owner

	def getstate(self):
		return self.state

	def setname(self,name1):
		self.name=name1
	
	def setstate(self,state1):
		self.state=state1
	
	def setowner(self,owner1):
		self.owner=owner1
	

	def toDict(self):
		d={}
		d['id']=self.id
		d['name']=self.name
		d['state']=self.state
		d['owner']=self.owner
		d['auth_token']=self.auth_token
		return d

	@classmethod
	def rowtoObj(cls,row):
		d=Device()
		d.id=row[0]
		d.name=row[1]
		d.state=bool(row[2])
		d.owner=int(row[3])
		d.auth_token=row[4]
		return d


	@classmethod
	def getDeviceById(cls,id1):
		dao=DAOClass()
		sql="select * from devices where id='"+id1+"'"
		print(sql)
		rows=dao.getData(sql)
		print(rows)
		if(rows==None):
			msg="Database Error"
			print(msg)
			return msg
		elif (rows==[]):
			msg="Device Not Found"
			print(msg)
			return msg
		else:
			r=cls.rowtoObj(rows[0])
			print(r)
			return r

	@classmethod
	def getDevicesByOwner(cls,owner1):
		dao=DAOClass()
		sql="select * from devices where owner="+str(owner1)
		print(sql)
		rows=dao.getData(sql)
		print(rows)
		if(rows==None):
			msg="Database Error"
			print(msg)
			return msg
		elif (rows==[]):
			msg="No Devices Found"
			print(msg)
			return msg
		else:
			r=[cls.rowtoObj(row) for row in rows]
			print(r)
			return r

	@classmethod
	def deleteDeviceById(cls,id1):
		dao=DAOClass()
		sql="delete from sessions where device_id='"+id1+"'"
		print(sql)
		r=dao.updateData(sql)
		sql="delete from devices where id='"+id1+"'"
		print(sql)
		r=dao.updateData(sql)
		print(r)
		return r
			

	def addDevice(self):
		dao=DAOClass()
		sql="select * from devices where owner="+str(self.owner)+" and name='"+self.name+"'"
		print(sql)
		rows=dao.getData(sql)
		print(rows)
		if(rows==[]):
			sql="insert into devices(id,name,state,owner,authtoken) values('"+self.id+"','"+self.name+"',"+str(int(self.state))+","+str(self.owner)+",'"+self.auth_token+"')"
			print(sql)
			r=dao.updateData(sql)
			if(r==True):
				return r
			else:
				msg="Database Error"
				print(msg)
				return msg

		elif(rows==None):
			msg="Database Error"
			print(msg)
			return msg
		else:
			msg="Another Device having same name found."
			print(msg)
			return msg

	@classmethod
	def updateDeviceStateById(cls,id1,state1):
		dao=DAOClass()
		sql="update devices set state="+str(int(state1))+" where id='"+id1+"'"
		print(sql)
		r=dao.updateData(sql)
		return r


	def updateDevice(self):
		dao=DAOClass()
		sql="select * from devices where owner="+str(self.owner)+" and name='"+self.name+"'"
		print(sql)
		rows=dao.getData(sql)
		print(rows)
		if(rows==[]):
			sql="update devices set name='"+self.name+"' where id='"+self.id+"'"
			print(sql)
			r=dao.updateData(sql)
			if(r==True):
				return r
			else:
				msg="Database Error"
				print(msg)
				return msg

		elif(rows==None):
			msg="Database Error"
			print(msg)
			return msg
		else:
			msg="Another Device having same name found."
			print(msg)
			return msg



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
		sql="select * from users where id="+str(id1)
		print("getUserById: "+sql)
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
		sql="update users set name='"+self.name+"', email='"+self.email+"', pwd='"+self.pwd+"' where id="+self.id
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


class Session():
	def __init__(self,device_id=None,st_time=None):
		self.id=0
		self.deviceid=device_id
		self.start_time=st_time
		self.end_time=None
		self.energy_consumed=0

	def getid(self):
		return self.id

	def getdeviceid(self):
		return self.deviceid

	def getstarttime(self):
		return self.start_time

	def getendtime(self):
		return self.end_time

	def getenergyconsumed(self):
		return self.energy_consumed

	def setid(self,id1):
		self.id=id1

	def setendtime(self,endtime):
		self.end_time=endtime

	def setenergyconsumed(self,energyc):
		self.energy_consumed=energyc

	@classmethod
	def rowtoObj(cls,row):
		s=Session(row[1],row[2])
		s.id=row[0]
		s.end_time=row[3]
		s.energy_consumed=row[4]
		return s

	def toDict(self):
		s={}
		s['id']=self.id
		s['device_id']=self.deviceid
		s['start_time']=self.start_time
		s['end_time']=self.end_time
		s['energy_consumed']=self.energy_consumed
		return s


	@classmethod
	def getSessionsByDevice(cls,device_id):
		dao=DAOClass()
		sql="select * from sessions where device_id='"+device_id+"' and end_time is NOT NULL"
		print(sql)
		rows=dao.getData(sql)
		print(rows)
		if(rows==None):
			msg="Database Error"
			print(msg)
			return msg
		elif (rows==[]):
			msg="No Sessions Found"
			print(msg)
			return msg
		else:
			r=[cls.rowtoObj(row) for row in rows]
			print(r)
			return r

	@classmethod
	def getSessionById(cls,id1):
		dao=DAOClass()
		sql="select * from sessions where id="+id1
		print(sql)
		rows=dao.getData(sql)
		if(rows==None):
			msg="Database Error"
			print(msg)
			return msg
		elif (rows==[]):
			msg="Session Not Found"
			print(msg)
			return msg
		else:
			r=cls.rowtoObj(rows[0])
			print(r)
			return r

	
	def addSession(self):		
		dao=DAOClass()
		sql="insert into sessions(device_id,start_time) values('"+self.deviceid+"',now())"
		r=dao.updateData(sql)
		if(r==True):
			sql="select max(id) from sessions where device_id='"+self.deviceid+"' and end_time is NULL"
			rows=dao.getData(sql)
			if(rows==None):
				return "Database Error"
			else:
				self.id=rows[0][0]
				return int(self.id)
		else:
			return "Database Error"

	def updateSession(self):
		dao=DAOClass()
		sql="update sessions set end_time=now(), energy_consumed="+str(self.energy_consumed)+" where id="+str(self.id)
		print(sql)
		r=dao.updateData(sql)
		return r


	@classmethod
	def deleteSessionsByDevice(cls,device_id):
		dao=DAOClass()
		sql="delete from sessions where device_id='"+device_id+"'"
		print(sql)
		r=dao.updateData(sql)
		print(r)
		return r

	@classmethod
	def deleteSessionById(cls,id1):
		dao=DAOClass()
		sql="delete from sessions where id="+str(id1)
		print(sql)
		r=dao.updateData(sql)
		print(r)
		return r


	@classmethod
	def getEnergyConsumedPerDeviceByOwner(cls,owner,startdate=None,enddate=None,lastbilldate=None):
		def rowtoDict(row):
			r={}
			r['id']=row[0]
			r['name']=row[1]
			r['energyc']=row[2]
			return r

		dao=DAOClass()
		if(lastbilldate!=None):
			sql="select device_id,name,sum(energy_consumed) as esum \
			from sessions,devices \
			where sessions.device_id=devices.id \
			and start_time between '"+lastbilldate+"'+INTERVAL 1 DAY and now() \
			group by device_id \
			having device_id in (select id from devices where owner="+str(owner)+") \
			and esum is not null"
			
		elif(startdate!=None and enddate!=None and lastbilldate==None):
			sql="select device_id,name,sum(energy_consumed) as esum \
			from sessions,devices \
			where sessions.device_id=devices.id \
			and start_time between '"+startdate+"' and '"+enddate+"' \
			group by device_id \
			having device_id in (select id from devices where owner="+str(owner)+") \
			and esum is not null"
			
		else:
			msg="Query Error"
			print(msg)
			return msg
		
		print(sql)
		rows=dao.getData(sql)
		print(rows)
		if(rows==None):
			msg="Database Error"
			print(msg)
			return msg
		elif (rows==[]):
			msg="No Sessions of any Device Found!!!"
			print(msg)
			return msg
		else:
			r=[rowtoDict(row) for row in rows]
			print(r)
			return r

		

class UserSetting():
	def __init__(self,user_id,setting,value):
		self.user_id=user_id
		self.setting=setting
		self.value=value

	def setvalue(self,value):
		self.value=value

	def addSetting(self):
		dao=DAOClass()
		sql="insert into usersettings values("+str(self.user_id)+",'"+self.setting+"','"+self.value+"')"
		print(sql)
		r=dao.updateData(sql)
		return r

	def toDict(self):
		d={}
		d['user_id']=self.user_id
		d['setting']=self.setting
		d['value']=self.value
		return d

	@classmethod
	def rowtoObj(cls,row):
		us=UserSetting(row[0],row[1],row[2])
		return us

	@classmethod
	def getSetting(cls,user_id,setting):
		dao=DAOClass()
		sql="select * from usersettings where user_id="+str(user_id)+" and setting='"+setting+"'"
		print(sql)
		rows=dao.getData(sql)
		if(rows==None or rows==[]):
			return False
		else:
			return cls.rowtoObj(rows[0])

	
	@classmethod
	def getAllSettings(cls,user_id):
		dao=DAOClass()
		sql="select * from usersettings where user_id="+str(user_id)
		print(sql)
		rows=dao.getData(sql)
		if(rows==None or rows==[]):
			return False
		else:
			return [cls.rowtoObj(row) for row in rows]


	def updateSetting(self):
		dao=DAOClass()
		sql="update usersettings set svalue='"+self.value+"' where user_id="+str(self.user_id)+" and setting='"+self.setting+"'"
		print(sql)
		r=dao.updateData(sql)
		return r

	@classmethod
	def updateLastBillDate(cls,user_id):
		dao=DAOClass()
		sql="select svalue from usersettings where user_id="+user_id+" and setting='billingcycle'"
		print(sql)
		billingcycle=dao.getData(sql)[0][0]
		print(billingcycle)
		if(billingcycle==None):
			return False

		sql="update usersettings set svalue=svalue+INTERVAL "+billingcycle+" DAY\
		 where user_id="+user_id+" and setting='lastbilldate' \
		 and now()>svalue+INTERVAL "+billingcycle+" DAY"
		print(sql)
		r=dao.updateData(sql)
		return r

	@classmethod
	def getBillingPeriodDates(cls,user_id,billingcycle):
		dao=DAOClass()
		sql="select svalue+INTERVAL 1 DAY,svalue+INTERVAL "+str(billingcycle)+" DAY \
		 from usersettings where user_id="+str(user_id)+" and setting='lastbilldate'"
		print(sql)
		rows=dao.getData(sql)
		if(rows==None or rows==[]):
			return False
		else:
			return rows[0][0],rows[0][1]



class Notification():
	def __init__(self):
		self.id=None
		self.user_id=None
		self.time=None
		self.type=None
		self.msg=None
		self.readn=False

	def setuserid(self,user_id):
		self.user_id=user_id

	def settype(self,type1):
		self.type=type1

	def setmsg(self,msg):
		self.msg=msg
	

	def toDict(self):
		d={}
		d['id']=self.id
		d['user_id']=self.user_id
		d['time']=self.time
		d['type']=self.type
		d['msg']=self.msg
		d['readn']=self.readn
		return d

	@classmethod
	def rowtoObj(cls,row):
		n=Notification()
		n.id=row[0]
		n.user_id=int(row[1])
		n.time=row[2]
		n.type=row[3]
		n.msg=row[4]
		n.readn=bool(row[5])
		return n

	@classmethod
	def getNotificationsByUser(cls,user_id):
		dao=DAOClass()
		sql="select * from notifications where user_id="+str(user_id)
		print(sql)
		rows=dao.getData(sql)
		print(rows)
		if(rows==None):
			msg="Database Error"
			print(msg)
			return msg
		elif (rows==[]):
			msg="No Notifications Found"
			print(msg)
			return msg
		else:
			r=[cls.rowtoObj(row) for row in rows]
			print(r)
			return r	


	def addNotification(self):
		dao=DAOClass()
		sql="insert into notifications(user_id,time,type,msg,readn) \
		values("+str(self.user_id)+",now(),'"+self.type+"','"+self.msg+"',0)"
		
		print(sql)
		r=dao.updateData(sql)
		return r

	@classmethod
	def readNotification(cls,nid):
		dao=DAOClass()
		sql="update notifications set readn=1 where id="+str(nid)
		r=dao.updateData(sql)
		print(sql)
		return r

	@classmethod
	def getNotificationsByUserIdAndDates(cls,user_id,startdate,enddate):
		dao=DAOClass()
		sql="select * from notifications where user_id="+user_id+" \
		and time between '"+startdate+"' and '"+enddate+"'+INTERVAL 1 DAY"
		
		print(sql)
		rows=dao.getData(sql)
		print(rows)
		if(rows==None):
			msg="Database Error"
			print(msg)
			return msg
		elif (rows==[]):
			msg="No Notifications Found"
			print(msg)
			return msg
		else:
			r=[cls.rowtoObj(row) for row in rows]
			print(r)
			return r


