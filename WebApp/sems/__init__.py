from flask import Flask
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb as mysql

app=Flask(__name__)
 
# MySQL configurations
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'sems'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['SECRET_KEY']='\xfc\x185\xda\xe2\xc9n\xfd\xe4i\xfa\xb8E\x88\xabR\x8b\x0e\x99{\x11a\x96Y'



from sems import routes
