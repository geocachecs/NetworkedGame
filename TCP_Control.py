####### code syntax
###     "=*=*=:0012:0231"
### 	   "=*=*=:codenum:parameter1:parameter2:etc"
### 
###	   BYTES in code word should be: 15

####### Codes
### 11 == shutdown connection
### 0 == get input from client
### 1 == print text
### 2 == begin countdown

import socket
import time as tm


class Control:
	def __init__(self,client,server):
		self.codewordlength = 15
		self.codewordtemplate = "=*=*=:{:0>4}:{:0>4}"
		self.client = client
		self.server = server
		self.gotdata = True
		
		
	def _getdata(self,length):
		s = self.client.recv(length)
		return s.decode()
		
	def _senddata(self,s):
		self.client.send(s.encode())
		
	def _getcode(self):
		#codeline = self.client.recv(self.codewordlength)
		#codeline = (str(codeline)[2:])[:-1]
		codeline = self._getdata(self.codewordlength)
		invalidcode = Exception("Control._getcode(): invalid code '{}'".format(codeline))
		codeline = codeline.split(":")
		if(codeline[0]==""):
			return (-1,[-1])
		elif(codeline[0]!="=*=*="):
			raise invalidcode
		try:
			code = int(codeline[1])
		except:
			raise invalidcode
		params = [ int(i) for i in codeline[2:] ]
		return (code,params)
	
	def _createcodeword(self, code ,*params):
		if(len(params)==0):
			params = [0]
		return self.codewordtemplate.format(code,*params)
	
class Control_Server(Control):
	def __init__(self,client,server):
		super().__init__(client,server)
	
	def sendInputRequestAndReceive(self):
		codeword = self._createcodeword( 0, 0)
		self._senddata(codeword)
		_,textlength = self._getcode()
		s = self._getdata(textlength[0])
		return s
	
	def sendText(self,s):
		if(len(s)>9999):
			raise Exception("Control_Server: sendText(): string too large")
		codeword = self.codewordtemplate.format(1, len(s.encode()))
		self.client.send(codeword.encode())
		self.client.send(s.encode())
		
	def initiateCountDown(self,count):
		codeword = self._createcodeword(2,count)
		self._senddata(codeword)
		
		
	def closeConnection(self):
		codeword = self._createcodeword(11)
		self._senddata(codeword)
		self.client.close()
		

class Control_Client(Control):
	def __init__(self,client,server):
		super().__init__(client,server)
		
	def run_client(self,automate=[]):
		automate=automate[::-1]
		instring = None
		
		while(True):	
			code,params = self._getcode()
			if(code==11):
				self.client.shutdown(socket.SHUT_RDWR)
				self.client.close()
				break
			elif(code == 0):
				if(len(automate)>0):      
					instring = automate.pop()
				else:
					instring = None
				self.__getInputAndSend(instring)
			elif(code == 1):
				self.__printText(params)
			elif(code == 2):
				self.__doCountdown(params[0])
			else:
				raise Exception("Control_Client(): Unknown code: {}".format(code))

		
	def __getInputAndSend(self,instring=None):
		if(instring==None):
			s = input()
		else:
			s = str(instring)
		codeword = self._createcodeword(1,len(s))
		self._senddata(codeword)
		self._senddata(s)
		
		
	def __printText(self,params):
		print( str(self._getdata(params[0])) ,end="")
		
	def __doCountdown(self,count=10):
		print("Waiting for players")
		print("Countdown: {:>2}".format(str(count)),end="\r")
		mytime = tm.time()
		while(count>0):
			thistime = tm.time()
			if(thistime-mytime>1):
				mytime=thistime
				count-=1
				print("Countdown: {:>2}".format(str(count)),end="\r")
		
	def docommands(self,s):
		self.__askforinput(s)
		
		
		