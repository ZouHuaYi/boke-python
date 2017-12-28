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
from controll import login_required
from vcode import create_vcode_img
import config
import StringIO
from exit import db
from database import User,Classfiy,Article

app = Flask(__name__)
app.config.from_object(config) 
db.init_app(app)

#页面路由部分
@app.route('/')
def index():
	return 'hello word'

@app.route('/login/',methods=['GET','POST'])
def login():
	if request.method =='POST':
		data = request.form
		if data['username']== app.config['ADMIN'] and data['password']== app.config['PW'] and session.get('vcode') == data['vcode']:
			session['username'] = app.config['ADMIN']
			return redirect('admin',listid='all')
		else:	
			return redirect(url_for('login'))
	else:
		if session.get('username') != app.config['ADMIN']:
			return redirect(url_for('login'))
		else:
			return redirect('admin',listid='all')	

#验证登录
@app.route('/admin/<int:lid>/')
@login_required
def admin(lid=1):
	# if listid == 'all':
	#  	listdata = Article.query.all()
	#  	#listdata = Article.query.filter(Article.id = 1).all()	
		return render_template('www/list_item.html')	

#添加文章页面
@app.route('/additem/')
@login_required
def add_item():
	classfiy = Classfiy.query.all()
	return render_template('www/add_item.html',classfiy=classfiy)

#提交文章页
@app.route('/post/',methods=['GET','POST'])
def post():
	if request.method =='POST':
		data = request.form
		article = Article(title=data['title'],subtitle=data['subtitle'],brief=data['brief'],content=data['content'],key=data['key'],date=data['date'],category_id=data['category_id'])
		db.session.add(article)
		db.session.commit()
	return redirect(url_for('add_item'))

#导航钩子 钩子函数做登录限制会出现循环重定向的问题浏览器
# @app.before_request
# def login_bc():
# 	if session.get('username') is None:
# 		return redirect(url_for('login'))	

# #验证码
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