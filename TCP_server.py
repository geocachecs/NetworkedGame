import socket
from TCP_Control import *
import random
import threading
import time



numbergame_title_art = ''' _______               ___.                    ________                       
 \      \  __ __  _____\_ |__   ___________   /  _____/_____    _____   ____  
 /   |   \|  |  \/     \| __ \_/ __ \_  __ \ /   \  ___\__  \  /     \_/ __ \ 
/    |    \  |  /  Y Y  \ \_\ \  ___/|  | \/ \    \_\  \/ __ \|  Y Y  \  ___/ 
\____|__  /____/|__|_|  /___  /\___  >__|     \______  (____  /__|_|  /\___  >
        \/            \/    \/     \/                \/     \/      \/     \/ '''

	


def clientGame(control,svr_vars):
	keepalive = True
	control.sendText(numbergame_title_art + "\n\n")
	while(keepalive):
		time.sleep(.1)
		######## Player number incremented ##### Decrements to 0 later in loop
		svr_vars.numplayers+=1

		
		if(svr_vars.numplayers<2):
			control.sendText("Waiting for at least one additional player...\n")
		while(svr_vars.numplayers<2):
			time.sleep(.1)
		
		control.sendText("Alright, let's play!\nYou have {} seconds left in this game before the server reveals its number!\nInput a number between 1 and 100: ".format(svr_vars.timer))
	
		svr_vars.startgame=True  ####### START GAME
		
		response = control.sendInputRequestAndReceive()
		while(response.isnumeric() == False or 1>int(response)>10 ):
			control.sendText("\nHmm... the input is invalid. Remember, 1 to 10 only.\nInput a number between 1 and 10: ")
			print(response)
			response = control.sendInputRequestAndReceive()
		control.sendText("Your number is: {}\n".format(int(response)))
		
		control.initiateCountDown(int(svr_vars.timer) if svr_vars.timer > 0 else 0)
		while(svr_vars.timer>0):
			time.sleep(svr_vars.timer-.5 if svr_vars.timer-.5>0 else 0.1)
		
		######### End game ### server_run automatically ends game
		#svr_vars.startgame=False
		svr_vars.numplayers-=1
		##################
		
		servernumber = svr_vars.randomnum
		control.sendText("The server's number is: {}\n".format(servernumber))
		if(servernumber==int(response)):
			control.sendText("YOU WIN!!!!!!\n")
		
		 
		
		
		control.sendText("Would you like to play again? (Y)es/(N)o: ")
		response = control.sendInputRequestAndReceive()
		if(len(response)>0 and (response[0]=="Y" or response[0]=="y") ):
			pass
		else:
			keepalive=False
	control.closeConnection()



	

def run_server(svr_vars):
	svr_vars.randomnum = random.randint(1,100)
	while(True):
		if(svr_vars.startgame==True):
			thistime=time.time()
			while(svr_vars.timer>0):
				lasttime = thistime
				thistime=time.time()
				svr_vars.timer-=thistime-lasttime
				time.sleep(.2)
			svr_vars.randomnum = random.randint(1,100)
			svr_vars.startgame=False
			svr_vars.timer=30

close_server = False	
def server_console():
	while(True):
		print("Press q to close server: ",end="")
		user_in=input()
		if(user_in=="q" or user_in=="Q"):
			close_server=True
			
			
'''	
class SharedVars:
		def __init__(self,**kwargs):
			self.__kwargs=kwargs
			self.__locks = {}
			for key in kwargs:
				self.__locks[key]=threading.Lock()
				print(key)
		
		def getVar(self,varname):
			self.__locks[varname].acquire()
			x=self.__kwargs[varname]
			self.__locks[varname].release()
			return x
		def setVar(self,varname,value):
			self.__locks[varname].acquire()
			self.__kwargs[varname]=value
			self.__locks[varname].release()
		def incVar(self,varname,incAmount):
			self.__locks[varname].acquire()
			self.__kwargs[varname]+=incAmount
			self.__locks[varname].release()
		def opVar(self,varname,function,args):
			self.__locks[varname].acquire()
			self.__kwargs[varname].function(*args)
			self.__locks[varname].release()
'''

class SharedVariables:
	def __init__(self):
		self.__numplayers=0
		self.__numplayers_lock = threading.Lock()
		self.__timer=30
		self.__timer_lock = threading.Lock()
		self.__numConnections = []
		self.__numConnections_lock = threading.Lock()
		self.__startgame = False
		self.__startgame_lock = threading.Lock()
		self.__randomnum = 0
		self.__randomnum_lock = threading.Lock()
	@property
	def randomnum(self):
		self.__randomnum_lock.acquire()
		x=self.__randomnum
		self.__randomnum_lock.release()
		return x
	@randomnum.setter
	def randomnum(self,num):
		self.__randomnum_lock.acquire()
		self.__randomnum=num
		self.__randomnum_lock.release()
	@property
	def startgame(self):
		self.__startgame_lock.acquire()
		x=self.__startgame
		self.__startgame_lock.release()
		return x
	@startgame.setter
	def startgame(self,num):
		self.__startgame_lock.acquire()
		self.__startgame=num
		self.__startgame_lock.release()
	@property
	def numConnections(self):
		self.__numConnections_lock.acquire()
		x=self.__numConnections
		self.__numConnections.release()
		return x
	@numConnections.setter
	def numConnections(self,num):
		self.__numConnections_lock.acquire()
		self.__numConnections=num
		self.__numConnections_lock.release()
	@property
	def timer(self):
		self.__timer_lock.acquire()
		x=self.__timer
		self.__timer_lock.release()
		return x
	@timer.setter
	def timer(self,num):
		self.__timer_lock.acquire()
		self.__timer=num
		self.__timer_lock.release()
	@property
	def numplayers(self):
		self.__numplayers_lock.acquire()
		x=self.__numplayers
		self.__numplayers_lock.release()
		return x
	@numplayers.setter
	def numplayers(self,num):
		self.__numplayers_lock.acquire()
		self.__numplayers=num
		self.__numplayers_lock.release()
		



#################### INITIALIZE SERVER ################		

svr_vars = SharedVariables()

server_timer = threading.Thread(target=run_server, args=[svr_vars])
server_timer.daemon=True
server_timer.start()

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
host = "localhost"#socket.gethostname()
port = 1337
server.bind((host,port))
server.listen()

while(True):
	client,address = server.accept()
	t = threading.Thread(target=clientGame, args=[Control_Server(client,server),svr_vars])
	t.daemon = True
	#threadList.append(t)
	t.start()
	if(close_server==True):
		break

exit()


#print(address)
#client.send("x".encode())
#client.send("Hello, world!! LOL".encode())
#print(client.recv(20))
