import socket
from TCP_Control import Control_Client
import sys

def usage():
	print("usage: python {argv0} <host>".format(argv0=sys.argv[0]))
	exit()

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)

if(len(sys.argv)<2 or len(sys.argv)>2):
	usage()
	
targethost = sys.argv[1]
targetport = 1337


try:
	server = client.connect((targethost,targetport))
except:
	raise Exception("Did not connect")

client_ctrl = Control_Client(client,server)

client_ctrl.run_client()
