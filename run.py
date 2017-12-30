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
			return redirect(url_for('admin',lid='all'))
		else:	
			return	render_template('www/login.html')
	else:
		return	render_template('www/login.html')	

#验证登录
@app.route('/admin/<lid>/',methods=['GET','POST'])
@login_required
def admin(lid):
	if lid == 'all':
	  	listdata = Article.query.all()
	else:  	
	  	listdata = Article.query.filter(Article.category_id == lid).all()	
	classfiy = Classfiy.query.all()  	
	return render_template('www/list_item.html',listdata=listdata,classfiy=classfiy)	

#添加文章页面
@app.route('/additem/')
@login_required
def add_item():
	classfiy = Classfiy.query.all()
	return render_template('www/add_item.html',classfiy=classfiy)

#分类列表
@app.route('/list/')
@login_required
def add_list():
	classfiy = Classfiy.query.all()
	return render_template('www/add_list.html',classfiy=classfiy)

#添加分类
@app.route('/adclass/')
@login_required
def adclass():
	classfiy = Classfiy.query.all()
	return render_template('www/add_class.html',classfiy=classfiy)
	
#提交文章页
@app.route('/post/',methods=['POST'])
@login_required
def post():
	if request.method =='POST':
		data = request.form
		article = Article(title=data['title'],subtitle=data['subtitle'],brief=data['brief'],content= data['content'],key=data['key'],date=data['date'],category_id=data['category_id'])
		db.session.add(article)
		db.session.commit()
		return redirect(url_for('add_item'))
	else:	
		return redirect(url_for('login'))

#删除数据
@app.route('/delete/<l_id>/<d_id>/')
@login_required
def delete(l_id,d_id):
	article=Article.query.filter(Article.id == d_id).first()
	db.session.delete(article)
	db.session.commit()
	return redirect(url_for('admin',lid=l_id))

#修改内容
@app.route('/amend/<a_id>/')
@login_required
def amend(a_id):
	aitem=Article.query.filter(Article.id==a_id).first()
	classfiy = Classfiy.query.all()
	return render_template('www/amend_item.html',aitem=aitem,classfiy=classfiy)

#文件上传
@app.route('/upload/')
@login_required
def upload():
	pass
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