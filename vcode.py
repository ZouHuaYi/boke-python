# -*- coding:utf-8 -*-

import random
import Image, ImageDraw, ImageFont, ImageFilter
import math

_letter_cases = "abcdefghjkmnpqrstuvwxy"  				# 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper()  					# 大写字母
_numbers = ''.join(map(str, range(3, 10)))  			# 数字
init_chars = _letter_cases + _upper_cases + _numbers

class create_vcode_img():
	"""生成随机验证码"""
	def __init__(self,chart = init_chars,size = (120,30),
		mode = "RGB",
		bg_color = (230,230,230),
		fg_color = (18,18,18),
		font_size = 20,
		font_type = 'static/fonts/fzlttch.ttf',
		length = 4,
		draw_lines = True,
		n_line = (1,5),
		draw_points = True,
		point_chance = 1):
			self.chart = chart
			self.size = size
			self.width,self.height = size
			self.bg_color = bg_color
			self.fg_color = fg_color
			self.font_size = font_size
			self.font_type = font_type
			self.length = length
			self.draw_lines =draw_lines
			self.n_line = n_line
			self.draw_points = draw_points
			self.point_chance = point_chance
			self.img = Image.new(mode,size,bg_color)		 #创建图像    
			self.draw = ImageDraw.Draw(self.img)             #创建画笔

	def get_chart(self):
		#生成字符串
		return random.sample(self.chart,self.length)

	def rn_color(self):
		#生成随机颜色的函数
		return (random.randint(32,200),random.randint(60,250),random.randint(10,50))	
		
	def create_lines(self):
		#干扰线
		line_num = random.randint(*self.n_line)	
		for i in range(line_num):
			begin = (random.randint(0,self.width),random.randint(0,self.height))
			end = (random.randint(0,self.width),random.randint(0,self.height))
			self.draw.line([begin,end],fill = self.rn_color())

	def create_points(self):
		chance = min(100,max(0,int(self.point_chance)))			#大小在0-100
		for w in range(self.width):
			for h in range(self.height):
				tmp = random.randint(0,100)	
				if tmp > 100 - chance:
					self.draw.point((w,h),fill = self.rn_color())

	def create_strs(self):
		#绘制验证码字符	
		c_chart = self.get_chart()
		strs = ' %s ' % ' '.join(c_chart)
		font = ImageFont.truetype(self.font_type,self.font_size)
		font_width,font_height = font.getsize(strs)
		fx = self.width/self.length
		dx = (self.width - font_width)/self.length
		fy = math.fabs(self.height-font_height)
		for i in range(self.length):
			self.draw.text((fx*i+dx ,random.uniform(0,fy)), c_chart[i], font = font , fill = self.rn_color())
		return ''.join(c_chart)			

	def create_img(self):
		if self.draw_lines:
			self.create_lines()
		if self.draw_points:
			self.create_points()
		strs = self.create_strs()
		params = [1-float(random.randint(1,2))/100,0,0,0,1-float(random.randint(1, 10)) / 100,float(random.randint(1, 2)) / 500,0.001,float(random.randint(1, 2)) / 500]			
		img = self.img.transform(self.size, Image.AFFINE, params)   	# 创建扭曲
		img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)        				# 滤镜， 边界加强（ 阈值更大）
		return img, strs

# if __name__ == '__main__':
#   	vcode = create_vcode_img()
#   	img,strs = vcode.create_img()
# img.save('./test.png', 'PNG')
		
		

