# -*- coding:utf-8 -*-

DEBUG = True 		# 启动Flask的Debug模式
DRIVE = 'mysql'
USUER = 'root'
PASSWD = ''
LOCALHOST = 'localhost'
PORT = 3306
DATABASE = 'boke_py'



SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(DRIVE,USUER,PASSWD,LOCALHOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = True

#app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123@localhost:3306/test' 
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True 