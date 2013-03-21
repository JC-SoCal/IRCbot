## A Simple IRC bot by @JC_SoCal, follow me on Twitter!
## Version 0.5
## This version is an inital push for anyone who needs to
## send or receive data on an IRC Channel. Further considerations
## are for send and receive to be within their own threads and
## utilize queues to receive, transmit data. We'll see ...
##

import sys
import socket
import string
import Queue

class IRCBot():
	def __init__(self, host="", port="", nick="", ident="", realname="", channel="", owner=""):
		self.host = host
		self.port = port
		self.nick = nick
		self.ident = ident
		self.realname = realname
		self.channel = channel
		self.owner = owner

		self.s = socket.socket()

		self.transmitQueue = Queue.Queue()
		self.receiveQueue = Queue.Queue()

	def checkparams(self):
		pass
		#host, meh
		#port needs to be a number between 1 and 65435
		#nick 1-9 chars, numbers underscores (don't get crazy)
		#ident -- need to research wtf this is
		#realname -- chars with spaces (don't get crazy)
		#channel -- must start with a #, & + or ! AND chars, nums no spaces up to 50 len
		#owner -- follow the same rule as a nick

	def connect(self):		
		try:
			self.s.connect((self.host, self.port))
			self.s.send("NICK %s\r\n" % self.nick)
			self.s.send("USER %s %s bla :%s\r\n" % (self.ident, self.ident, self.realname))
			self.s.send("JOIN :%s\r\n" % self.channel)
		except socket.gaierror as detail:
			print "Error: Possible bad host name -", self.host, "Details:", detail

	def respondToPing(self, line):
		if (line[0] == "PING"):
			self.s.send("PONG %s\r\n" % line[1])
			return True 
		else: 
			return False

	def receive(self):
		readbuffer = ""
		readbuffer=readbuffer+self.s.recv(1024)
		temp=string.split(readbuffer, "\n")
		readbuffer=temp.pop()
		for line in temp:
			line=string.rstrip(line)
			line=string.split(line)
		self.respondToPing(line)
		return line

	def send(self, message):
		self.s.send("PRIVMSG %s :%s\r\n" % (self.channel, message))	
		
	def leave(self, message="Leaving Channel"):
		self.s.send("PART %s :%s ; testx\r\n" % (self.channel, message))

	def disconnect(self, message="Quitting"):
		self.s.send("QUIT :%s ; testx\r\n" % (message))
		self.s.shutdown(2)
		self.s.close()