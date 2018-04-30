from flask import Flask
import MySQLdb as mysql

app=Flask(__name__)
 
# MySQL configurations
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'tmp'
app.config['MYSQL_DATABASE_USER'] = 'sayan'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['SECRET_KEY']='\xfc\x185\xda\xe2\xc9n\xfd\xe4i\xfa\xb8E\x88\xabR\x8b\x0e\x99{\x11a\x96Y'



from sems import routes
