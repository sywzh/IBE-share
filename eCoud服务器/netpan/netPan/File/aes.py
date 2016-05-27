#-*-coding:utf8-*-

from Crypto.Cipher import AES

class mycrypt():
	def __init__(self,key):
		self.key = key
		self.mode = AES.MODE_CBC

	def myencrypt(self,text):
		cryptor = AES.new(self.key,self.mode)
		length = 32
		count = text.count('')
		if count < length:
			add = (length - count) + 1
			text = text + (' ' * add)
		elif count > length:
			add = (length - (count % length)) + 1
			text = text + (' ' * add)
		self.ciphertext = cryptor.encrypt(text)
		return self.ciphertext

	def mydecrypt(self,text):
		cryptor = AES.new(self.key,self.mode)
		plain_txt = cryptor.decrypt(text)
		return plain_txt

if __name__ == "__main__":
	#text = "98789khjsajfilahfpoiwufipoasufipo"
	fp = open('2.pdf','rb')
	text = fp.read()
	fp.close()
	key = "9878*(&^^&)0LLIu(*&^))#$@!KJLKJj"
	en = mycrypt(key)
	entext = en.myencrypt(text)
	detext = en.mydecrypt(entext).rstrip()
	fp = open('3.pdf','wb')
	fp.write(detext)
	fp.close()
