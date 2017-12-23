#!/usr/bin/env python
# coding:utf8

import sys
reload(sys)
sys.setdefaultencoding( "utf8" )

"""
__author__="zhy"
__mtime__ = '2017/12/18'
"""

from flask import *
from flask_sqlalchemy import SQLAlchemy
import MySQLdb
from vcode import create_vcode_img
import config
import StringIO

app = Flask(__name__)
app.config.from_object(config) 

#实例化
db = SQLAlchemy(app)

class User(db.Model):
	"""用户数据表"""
	__tablename__ = 'user'
	id = db.Column(db.Integer,primary_key = True)
	username = db.Column(db.String(80),nullable = False,unique = True)
	password = db.Column(db.String(32),nullable = False)

	def __repr__(self):
		return '<User %r>' % self.username

db.create_all()

#页面路由部分
@app.route('/')
def index():
	return "Hello World!"

@app.route('/login/',)
def login():
	return render_template('www/login.html')

#验证登录
@app.route('/admin/', methods=['post'])
def admin():
	data = request.form
	
	


	
	print data['username']
	return render_template('www/login.html')

#验证码
@app.route('/vcode/')
def v_code():
	vcode = create_vcode_img()
	img,strs = vcode.create_img()
	buf = StringIO.StringIO() 
	img.save(buf,'JPEG',quality= 70)
	buf_str = buf.getvalue() 
	response = app.make_response(buf_str) 
	response.headers['Content-Type'] = 'image/jpeg' 
	return response


if __name__ == '__main__':
	app.run()