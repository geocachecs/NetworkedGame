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
		#svr_vars.numplayers+=1
		svr_vars.incVar("numplayers",1)
		
		#while(svr_vars.numplayers<2):
		#	time.sleep(.1)
		while(svr_vars.getVar("numplayers")<2):
			time.sleep(.1)
	
		#control.initiateCountDown()
		
		control.sendText("Alright, let's play!\nYou have {} seconds left in this game before the server reveals its number!\nInput a number between 1 and 100: ".format(svr_vars.timer))
		response = control.sendInputRequestAndReceive()
		while(response.isnumeric() == False or 1>int(response)>10 ):
			control.sendText("\nHmm... the input is invalid. Remember, 1 to 10 only.\nInput a number between 1 and 10: ")
			print(response)
			response = control.sendInputRequestAndReceive()
		control.sendText("Your number is: {}\n".format(int(response)))
		servernumber = random.randint(1,10)
		
		#while(svr_vars.timer>0):
		#	control.sendText("{} seconds until the server reveals its number!\r".format(svr_vars.timer))
		#	time.sleep(.5)
			
		
		control.sendText("The server's number is: {}\n".format(servernumber))
		if(servernumber==int(response)):
			control.sendText("YOU WIN!!!!!!\n")
		
		######### Player number decremented 
		svr_vars-=1
		
		control.sendText("Would you like to play again? (Y)es/(N)o: ")
		response = control.sendInputRequestAndReceive()
		if(len(response)>0 and (response[0]=="Y" or response[0]=="y") ):
			pass
		else:
			keepalive=False
	control.closeConnection()


close_server = False	
	
def getInputToClose():
	global close_server
	while(True):
		
		print("Type 'Q' to close the server: ",end="")
		u_in = input()
		if(u_in[0]=='q' or u_in[0]=='Q'):
			close_server=True
	
def serverGame(svr_vars):
	while(True):
		pass
		
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


class SharedVariables:
	def __init__(self):
		self.__numplayers=0
		self.__numplayers_lock = threading.Lock()
		self.__timer=20
		self.__timer_lock = threading.Lock()
		self.__numConnections = []
		self.__numConnections = threading.Lock()
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
		
		
def server_timer(svr_vars):
	while(svr_vars.timer>0):
		svr_vars.timer-=1
		timer.sleep(1)


#################### INITIALIZE SERVER ################		

#svr_vars = SharedVariables()
svr_vars = SharedVars(timer=20,numplayers=0)

#svr_vars.timer = 20
#svr_vars.numplayers=0

#timer=threading.Thread(target=server_timer,args=[svr_vars])


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
host = socket.gethostname()
port = 1337
server.bind((host,port))
server.listen()

while(True):
	client,address = server.accept()
	t = threading.Thread(target=clientGame, args=[Control_Server(client,server),svr_vars])
	t.daemon = True
	#threadList.append(t)
	t.start()
	print(close_server)
	if(close_server==True):
		break

exit()


#print(address)
#client.send("x".encode())
#client.send("Hello, world!! LOL".encode())
#print(client.recv(20))
