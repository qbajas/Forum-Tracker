 #!/usr/bin/env python
 # -*- coding: utf-8 -*-


"""
Copyright (c) 2011, GrupaZP
 All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

     
import socket, threading, tracker
import pickle
httphost = "localhost:9999"
sockethost = "localhost:10001"

 
def handle(s, addr):
  #tak wg specyfikacji protokołu wygląda handshake, gdzie:
  #WebSocket-Origin - tutaj siedzi nasz serwer docelowy, w naszym przypadku serwer http
  #WebSocket-Location: - tutaj mamy nasz socket
  handshake = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n\
				Upgrade: WebSocket\r\n\
				Connection: Upgrade\r\n\
				WebSocket-Origin: http://%s\r\n\
				WebSocket-Location: ws://%s/\r\n\
				WebSocket-Protocol: sample\r\n\r\n" % (httphost, sockethost)
  s.send(handshake)
  data = s.recv(1024)
  lock = threading.Lock()
 
  while 1:
	#dostajemy paczkę danych od klienta, specyfikacja wymaga, by dane odbierane i wysyłane zaczynały się 
	#i kończyły odpowiednio znakami: '\x00' i \xff'
	data = s.recv(1024)
	if not data: break
	msg = data.split('\xff')[0][1:]
	print 'Data from', addr, ':', msg
	try:
		option, req = msg.split('###')
		answer = {
			'askGoogle' : askGoogle,
			'getSections' : getSections,
		}.get(option)(req,lock,s)
	except ValueError:
		pass

 
  print 'Client closed:', addr
  lock.acquire()
  clients.remove(s)
  lock.release()
  s.close()
 
def askGoogle(req,lock,s):
"""Wyslanie zapytania do Google"""
	tls.firstSiteLinks = trac.askGoogle(req)
#        print '\n'.join([item.encode('utf8') + ' ' + stat for item in tls.firstSiteLinks for stat in trac.getSerializedStats(tls.firstSiteLinks)])
#        linkstat = map(lambda a,b: a.encode('utf8') + ' ' + b, tls.firstSiteLinks, trac.getSerializedStats(tls.firstSiteLinks))
        linkstat = [(link, trac.getStats(link)) for link in tls.firstSiteLinks] # wysyłamy strony razem ze statsami w formie (link, [(ocena, data), (ocena, data)...])
	lock.acquire()
	s.send('\x00' + pickle.dumps(linkstat) +  '\xff')
	lock.release()
	
def getSections(req,lock,s):
	sections = trac.openForum(tls.firstSiteLinks[int(req)-1])
	lock.acquire()
	s.send('\x00' + "\n".join(sections).encode('utf8') +  '\xff')
	lock.release()
	
def start_server():
"""Uruchamia serwer."""
 s = socket.socket()
 s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 s.bind(('', 10001))
 s.listen(1)
 while 1:
   conn, addr = s.accept()
   print 'Connected by', addr
   clients.append(conn)
   threading.Thread(target = handle, args = (conn,addr)).start()
 
tls = threading.local()
clients = []
trac = tracker.Tracker()
start_server()

