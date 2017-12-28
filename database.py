# coding:utf8


from exit import db
from datetime import datetime
 
class User(db.Model):
	"""管理员账号表"""
	__tablename__ = 'user'
	id = db.Column(db.Integer,primary_key = True)
	username = db.Column(db.String(80),nullable = False,unique = True)
	password = db.Column(db.String(32),nullable = False)

class Article(db.Model):
		"""存储文章内容表"""
		__tablename__ = 'article'
		id = db.Column(db.Integer,primary_key=True,autoincrement=True)
		title = db.Column(db.String(30),nullable=False)
		subtitle = db.Column(db.String(150))
		brief = db.Column(db.String(255))
		content =db.Column(db.Text) 
		date = db.Column(db.DateTime,nullable=False,default=datetime.now)
		key = db.Column(db.String(30))
		volume = db.Column(db.Integer,nullable=False,default=0)
		category_id = db.Column(db.Integer,db.ForeignKey("classfiy.id"))
		category = db.relationship("Classfiy",backref=db.backref('articles'))

class Classfiy(db.Model):
			"""文章分类的表"""
			__tablename__ = 'classfiy'
			id = db.Column(db.Integer,primary_key=True,autoincrement=True)
			list_title = db.Column(db.String(30),nullable=False)
			height_light = db.Column(db.Integer,default =0)

