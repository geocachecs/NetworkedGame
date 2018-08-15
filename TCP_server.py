import socket
from TCP_Control import *
import random
import threading


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
host = socket.gethostname()
port = 1337

numbergame_title_art = ''' _______               ___.                    ________                       
 \      \  __ __  _____\_ |__   ___________   /  _____/_____    _____   ____  
 /   |   \|  |  \/     \| __ \_/ __ \_  __ \ /   \  ___\__  \  /     \_/ __ \ 
/    |    \  |  /  Y Y  \ \_\ \  ___/|  | \/ \    \_\  \/ __ \|  Y Y  \  ___/ 
\____|__  /____/|__|_|  /___  /\___  >__|     \______  (____  /__|_|  /\___  >
        \/            \/    \/     \/                \/     \/      \/     \/ '''

		
def playGame(control):
	keepalive = True
	control.sendText(numbergame_title_art + "\n\n")
	while(keepalive):
		control.initiateCountDown()
		control.sendText("Alright, let's play!\nInput a number between 1 and 10: ")
		response = control.sendInputRequestAndReceive()
		while(response.isnumeric() == False or 1>int(response)>10 ):
			control.sendText("\nHmm... the input is invalid. Remember, 1 to 10 only.\nInput a number between 1 and 10: ")
			print(response)
			response = control.sendInputRequestAndReceive()
		control.sendText("Your number is: {}\n".format(int(response)))
		servernumber = random.randint(1,10)
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


close_server = False	
	
def getInputToClose():
	global close_server
	while(True):
		
		print("Type 'Q' to close the server: ",end="")
		u_in = input()
		if(u_in[0]=='q' or u_in[0]=='Q'):
			close_server=True

serverconsole = threading.Thread(target=getInputToClose)
serverconsole.daemon = True
serverconsole.start()			
			
server.bind((host,port))
server.listen(2)

while(True):
	client,address = server.accept()
	t = threading.Thread(target=playGame, args=[Control_Server(client,server)])
	t.daemon = True
	t.start()
	print(close_server)
	if(close_server==True):
		break

exit()


#print(address)
#client.send("x".encode())
#client.send("Hello, world!! LOL".encode())
#print(client.recv(20))
