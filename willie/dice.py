from willie import module
from random import randint
import MySQLdb as mdb
import sys
import re

@module.commands('dice')
def dice (bot, trigger):
	try:
		con = mdb.connect('localhost', 'casino', 'btncasino', 'casino');
		
	except:
		print "Error: Unable to connect to DB."
		bot.say("Error: Unable to connect to DB.")
		return

	nick = trigger.nick
	cur = con.cursor()
	cur.execute("SELECT u.btn_id, w.balance FROM user u, wallet w WHERE u.nick = '" + nick + "' AND w.id = u.btn_id;")
		
	row = cur.fetchone()
	if row is None:
		bot.say(nick + " does not exist in the database.")
		return
	elif trigger.group(3) and trigger.group(4):
		id = str(row[0])
		balance = int(row[1])
		amt2, bet = trigger.group(2).split(None, 1)
		amt = int(amt2)
		if amt > balance:
			bot.say("You have not entered a valid amount, please try again.")
			return
		elif bet == 'high' or bet == 'low' :
			d1 = randint(1,6)
			d2 = randint(1,6)
			d3 = randint(1,6)
			sum = d1 + d2 + d3
			if sum >= 10:
				result = 'high'
			else:
				result = 'low'
			t1 = d1, d2, d3
			t2 = sum, result
			s1 = str(t1)
			s2 = str(t2)
			s3 = re.sub("[^a-zA-Z1-9, ]","", s2)
			if bet == result:
				nb = balance + amt
				bot.say(s1 + " is " + s3 + ". You win " + amt2 + ".")
			else:
				nb = balance - amt
				bot.say(s1 + " is " + s3 + ". You lose " + amt2 + ".")
			nb2 = str(nb)
			cur.execute("UPDATE wallet SET balance = '" + nb2 + "' WHERE id = '" + id + "';")
			con.commit()
			return
		else:
			bot.say("Please enter your bet in the form of .dice <amount> <high/low>")
			return
	else:
		bot.say("Please enter your bet in the form of .dice <amount> <high/low>")
		return
	con.close()
