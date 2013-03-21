## sample use file for ircbot class
import IRCbot
import time

def main():
	owner = "UrNick" #name of the nick who can send the !Quit command #doesn't work yet
	host = "irc.freenode.net"
	port = 6667
	nick = "JCbot"
	ident = "JCbot"
	realname = "JCbot"
	chan = "#linux"		

	bot = IRCbot.IRCBot(host,port,nick,ident,realname,chan,owner)
	bot.connect()

	loopCount = 1
	while 1:
		print bot.receive()
		bot.send("Current loop count: %s | sleeping 3 seconds ..." % (loopCount))
		time.sleep(3) # this is just so you don't flood the channel in the loop, you may not want this
		loopCount += 1
	
	bot.leave()
	bot.disconnect

if __name__ == "__main__":
	main()