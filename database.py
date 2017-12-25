# coding:utf8


from exit import db
 
class User(db.Model):
	"""用户数据表"""
	__tablename__ = 'user'
	id = db.Column(db.Integer,primary_key = True)
	username = db.Column(db.String(80),nullable = False,unique = True)
	password = db.Column(db.String(32),nullable = False)