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
from flask import Flask,render_template,request,session,redirect,url_for,make_response,g
from controll import login_required
from vcode import create_vcode_img
import config
import StringIO
from exit import db
from database import User,Classfiy,Article,Picture
import time
import Image
from werkzeug import secure_filename

#修改static为文件的默认路径
#app = Flask(__name__,static_folder='', static_url_path='')
app = Flask(__name__) 
app.config.from_object(config) 
db.init_app(app)
v_code_img = ''

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

#print time.strftime(r"%Y-%m-%d_%H-%M-%S",time.localtime())
#print time.time()*1000

#页面路由部分
@app.route('/')
def index():
	s=class_do()
	return render_template('www/test.html',sl=s)
#删除cookie
def delete_cookie(c_name):
	resp = make_response("delete cookie ok")
	resp.set_cookie('Name','',expires=-1) 
	return resp
	
#登录页面的逻辑
@app.route('/login/',methods=['GET','POST'])
def login():
	if request.method =='POST':
		global v_code_img
		data = request.form
		if data['username']== app.config['ADMIN'] and data['password']== app.config['PW'] \
		 and v_code_img == data['vcode'].lower():
			session['username'] = app.config['ADMIN']
			return redirect(url_for('admin',lid='all'))
		else:	
			return	render_template('www/login.html')
	else:
		return	render_template('www/login.html')	
#退出登录
@app.route('/del_cookie/')
def getout():
	session.clear()
	return redirect(url_for('login'))

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
			filename = secure_filename(f.filename)
			isImage,f_src = allowed_file(filename)
			if isImage:
				src_str = create_img_name(str='o',ext=f_src)
				src_thu = create_img_name(str='t',ext=f_src)
				print src_str
        		f.save(src_str)
        		create_thumbnail(ori_img=src_str,dst_img=src_thu,dst_w=168,dst_h=168,save_q=75)
        		pic=Picture(big_pic=src_str.replace(app.config['ROOT_PATH'],''),thumb_pic=src_thu.replace(app.config['ROOT_PATH'],''))
        		pic.db_add(pic)
	return 'success upload'

#新建文件夹
def make_folder():
	folder = time.strftime(r"%Y_%m",time.localtime())
	if  os.path.exists(r'%s/%s'%(app.config['UPLOADED_PATH'],folder)) == False:
		os.makedirs(r'%s/%s'%(app.config['UPLOADED_PATH'],folder))
	return 	r'%s/%s'%(app.config['UPLOADED_PATH'],folder)
#判断图片的类型
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return ('.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS,filename.rsplit('.', 1)[1])
#图片名字生成函数
def create_img_name(str,ext):
	return os.path.join(make_folder(),'%s_%s.%s'%(int(time.time()),str,ext))
#生成图片存储的路径
print create_img_name('0','jpeg')
#图片处理的所有函数
def create_thumbnail(**args):
	args_key = {"ori_img":"","dst_img":"","dst_w":"","dst_h":"","save_q":75}
	arg = {}
	for key in args_key:
		if key in args:
			arg[key]=args[key]

	im = Image.open(arg['ori_img'])
	ori_w,ori_h = im.size
	widthRatio = heightRatio = None
	ratio = 1
	if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):	

		if arg['dst_w'] and ori_w > arg['dst_w']:
			widthRatio = float (arg['dst_w'])/ori_w
		if arg['dst_h'] and ori_h > arg['dst_h']:
			heightRatio = float(arg['dst_h'])/ori_h

		if widthRatio and heightRatio:
			if widthRatio < heightRatio:
				ratio = widthRatio
			else:
				ratio = heightRatio

		if widthRatio and not heightRatio:
			ratio = widthRatio
		if heightRatio and not widthRatio:
			ratio = heightRatio

		newWidth = int(ori_w*ratio)
		newHeight = int(ori_h*ratio)
	else:
		newWidth = ori_w
		newHeight = ori_h

	im.resize((newWidth,newHeight),Image.ANTIALIAS).save(arg['dst_img'],quality=arg['save_q'])										


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
	global v_code_img
	v_code_img = strs.lower()
	return response

if __name__ == '__main__':
	app.run()