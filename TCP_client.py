import socket
from TCP_Control import Control_Client


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)

targethost = socket.gethostname()
targetport = 1337


try:
	server = client.connect((targethost,targetport))
except:
	raise Exception("Did not connect")

client_ctrl = Control_Client(client,server)

client_ctrl.run_client()
