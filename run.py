#!/usr/bin/env python
# coding:utf8

import sys
import os
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
import time

app = Flask(__name__)
app.config.from_object(config) 
db.init_app(app)\

#处理无限级分类的函数
def class_do():
	l={"son":{},"id":{}}
	classfiy = Classfiy.query.all()
	for value in classfiy:
		l["id"][value.id]=value
		if l['son'].get(value.p_id):
			l['son'][value.p_id].append(value.id)  	
		else:
			l['son'][value.p_id]=[value.id]  		
	return l

print time.strftime(r"%Y-%m-%d_%H-%M-%S",time.localtime())
print time.time()*1000
#新建文件夹
def make_folder():
	folder = time.strftime(r"%Y_%m",time.localtime())
	if  os.path.exists(r'%s/%s'%(app.config['UPLOADED_PATH'],folder)) == False:
		os.makedirs(r'%s/%s'%(app.config['UPLOADED_PATH'],folder))
		

make_folder()		

#页面路由部分
@app.route('/')
def index():
	s=class_do()
	return render_template('www/test.html',sl=s)
	
#登录页面的逻辑
@app.route('/login/',methods=['GET','POST'])
def login():
	if request.method =='POST':
		data = request.form
		if data['username']== app.config['ADMIN'] and data['password']== app.config['PW'] \
		 and session.get('vcode') == data['vcode']:
			session['username'] = app.config['ADMIN']
			return redirect(url_for('admin',lid='all'))
		else:	
			return	render_template('www/login.html')
	else:
		return	render_template('www/login.html')	

#验证登录
@app.route('/admin/',methods=['GET','POST'])
@app.route('/admin/<lid>/',methods=['GET','POST'])
@app.route('/admin/<lid>/<page>',methods=['GET','POST'])
@login_required
def admin(lid='all',page=1):
	if lid == 'all':
	  	listdata = Article.query.order_by(db.desc(Article.date)).paginate(int(page),2,error_out=False)
	else:  	
	  	listdata = Article.query.filter(Article.category_id == Classfiy.query.filter( Classfiy.key_str ==lid ).first().id) \
	  	.order_by(db.desc(Article.date)).paginate(int(page),2,error_out=False)
	classfiy = class_do()
	return render_template('www/list_item.html',listdata=listdata,classfiy=classfiy,lid=lid)	

#添加文章页面
@app.route('/additem/')
@login_required
def add_item():
	classfiy = class_do()
	return render_template('www/add_item.html',classfiy=classfiy)

#分类列表
@app.route('/list/')
@login_required
def add_list():
	classfiy = class_do()
	return render_template('www/list_class.html',classfiy=classfiy)

#添加分类 添加分类的数据
@app.route('/adclass/',methods=['GET','POST'])
@login_required
def adclass():
	if request.method=='POST':
		data = request.form
		classfiy = Classfiy(p_id=data['p_id'],list_title=data['l_title'],key_str=data['l_str'],son=None)
		db.session.add(classfiy)
		db.session.commit()
		return redirect(url_for('add_list'))
	else:
		classfiy =Classfiy.query.all()
		return render_template('www/add_class.html',classfiy=classfiy)

#提交文章页
@app.route('/post/',methods=['POST'])
@login_required
def post():
	if request.method =='POST':
		data = request.form
		article = Article(title=data['title'],subtitle=data['subtitle'],brief=data['brief'],content= data['content'],\
			key=data['key'],date=data['date'],category_id=data['category_id'])
		db.session.add(article)
		db.session.commit()
		return redirect(url_for('admin',lid='all'))
	else:	
		return redirect(url_for('login'))

#修改文章
@app.route('/change/',methods=['POST'])
@login_required
def change():
	data = request.form
	res=Article.query.filter(Article.id==data['id_title']).first()
	res.title = data['title']
	res.subtitle = data['subtitle']
	res.brief = data['brief']
	res.content = data['content']
	res.key = data['key']
	res.date = data['date']
	res.category_id = data['category_id']
	db.session.commit()
	return redirect(url_for('admin',lid=res.category.key_str))

#删除数据
@app.route('/delete/<l_id>/<d_id>/<b_id>')
@login_required
def delete(l_id,d_id,b_id):
	article=Article.query.filter(Article.id == d_id).first()
	db.session.delete(article)
	db.session.commit()
	return redirect(url_for("admin",lid=l_id,page=b_id))

#修改内容
@app.route('/amend/<a_id>/')
@login_required
def amend(a_id):
	aitem=Article.query.filter(Article.id==a_id).first()
	classfiy = class_do()
	return render_template('www/change_item.html',aitem=aitem,classfiy=classfiy)

#文件上传
@app.route('/upload/',methods=['POST'])
@login_required
def upload_file():
	if request.method == 'POST':
		for f in request.files.getlist('file'):
	        	f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
	return 'success upload'

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