# -*- coding: UTF-8 -*-
import random, string

def getRandomWord(self,count = 10,type = 'ZH'):
	#ZH:汉字；EN:字目；NUM:数字；NO:符号
	def getZH():
		head = random.randint(0xB0, 0xD7)
		body = random.randint(0xB0, 0xF7)
		val = ( head << 8 ) | (body)
		str = "%x" % val
		return str.decode('hex').decode('gb2312').encode('utf8')

	def getEN():
		return random.choice(string.ascii_letters)

	def getNUM():
		return random.choice(string.digits)

	def getNO():
		return random.choice(string.punctuation)

	tmp = ''
	for x in xrange(count):
		tmp += eval('get%s()'%type)
	return tmp

print getRandomWord(10)
