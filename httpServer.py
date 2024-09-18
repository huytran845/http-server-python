import socket

#Declaring the host and port of the server
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

#Creating the socket with the socket library
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is for IPv4 adress, and SOCK_STREAM represents TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...\n' % SERVER_PORT)

while True:    
	#Wait for client connections
	client_connection, client_address = server_socket.accept()

	#Get the client request
	request = client_connection.recv(1024).decode() #1024 is buffer size, and can be changed based on network conditions and data amount being worked with.
	print(request)

	#If request is EXIT, close the server
	if 'EXIT' in request:
		print('Shutting off server\n')
		break

	#Parse HTTP Headers
	headers = request.split('\n') #Split the header information by line
	pagename = headers[0].split()[1] #Select the first header and split it, choosing the 2nd element

	#Get Contents of file
	if pagename == '/':
		pagename = '/index.html'

	if pagename == '/favicon.ico': #Checks if page is trying to access favicon, since we don't have one, close that request
		client_connection.close()
		continue

	pagename = pagename.replace('/','')
	try: 
		page = open(pagename)
		content = page.read()
		page.close()

		response = 'HTTP/1.0 200 OK\n\n' + content
	
	except FileNotFoundError: #If the above code fails due to non-existent page, respond with error 404
		response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
	
	#Send HTTP response
	client_connection.sendall(response.encode())
	client_connection.close()

#Close socket
server_socket.close()