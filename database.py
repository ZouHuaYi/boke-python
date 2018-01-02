# coding:utf8


from exit import db
 
#基础数据库 可以省掉子类的 __table_args__ 了
class Base (db.Model):
    __abstract__ = True
    __table_args__ = { 
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
	} 

#用户 
class User(db.Model):
	"""管理员账号表"""
	__tablename__ = 'user'
	id = db.Column(db.Integer,primary_key = True)
	username = db.Column(db.String(80),nullable = False,unique = True)
	password = db.Column(db.String(32),nullable = False)

#文章
class Article(Base):
		"""存储文章内容表"""
		__tablename__ = 'article'
		id = db.Column(db.Integer,primary_key=True,autoincrement=True)
		title = db.Column(db.String(30))
		subtitle = db.Column(db.String(150))
		brief = db.Column(db.String(255))
		content =db.Column(db.Text) 
		date = db.Column(db.TIMESTAMP,server_default=db.func.now())
		key = db.Column(db.String(30))
		volume = db.Column(db.Integer,nullable = False,server_default='0')
		category_id = db.Column(db.Integer,db.ForeignKey("classfiy.id"))
		category = db.relationship("Classfiy",backref=db.backref('articles'))

#父级分类
class Classfiy(db.Model):
			"""文章分类的表"""
			__tablename__ = 'classfiy'
			id = db.Column(db.Integer,primary_key=True,autoincrement=True)
			p_id = db.Column(db.Integer,primary_key=True,server_default='0')
			list_title = db.Column(db.String(30),nullable=False)
			key_str = db.Column(db.String(30),nullable=False,unique=True,index=True) 
			height_light = db.Column(db.Integer,server_default='0')

	



