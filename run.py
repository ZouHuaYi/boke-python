#!/usr/bin/env python
# coding:utf8

import sys
reload(sys)
sys.setdefaultencoding( "utf8" )

"""
__author__="zhy"
__mtime__ = '2017/12/18'
"""

from flask import Flask,render_template,request,session,redirect,url_for
from vcode import create_vcode_img
import config
import StringIO
from exit import db

app = Flask(__name__)
app.config.from_object(config) 
db.init_app(app)

#页面路由部分
@app.route('/')
def index():
	return 'hello word'

@app.route('/login/')
def login():
	return render_template('www/login.html')

#验证登录
@app.route('/admin/',methods=['GET','POST'])
def admin():
	if request.method =='POST':
		data = request.form
		if data['username']== app.config['ADMIN'] and data['password']== app.config['PW'] and session.get('vcode') == data['vcode']:
			session['username'] = app.config['ADMIN']
			return render_template('www/list_item.html')
		else:	
			return render_template('www/login.html')
	else:
		if session.get('username') == app.config['ADMIN']:
			return redirect(url_for('login'))
		else:
			return render_template('www/list_item.html')	

#添加文章页面
@app.route('/additem/')
def add_item():
	return render_template('www/add_item.html')

#导航钩子
@app.before_request
def login_bc():
	if session.get('username') is None:
		return redirect(url_for('login'))	
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
	session['vcode'] = strs
	return response

if __name__ == '__main__':
	app.run()