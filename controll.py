# coding:utf8

from flask import session,url_for,redirect
from functools import wraps

#登录限制装饰器
def login_required(func):
	@wraps(func)
	def dec_func(*args, **kwargs):
		if session.get('username') is None:
			return redirect(url_for('login'))
		else:
			return func(*args, **kwargs)	
	return 	dec_func	

