from willie import module
import MySQLdb as mdb
import sys
import re

staff = 10

@module.commands('bal')
def bal (bot, trigger):
	try:
		con = mdb.connect('localhost', 'casino', 'btncasino', 'casino');
	except:
		print "Error: Unable to connect to DB."
		bot.say("Error: Unable to connect to DB.")
		return
	
	if trigger.group(2):
		nick = re.sub("[^a-zA-Z0-9]","", trigger.group(2))
		if nick == '':
			nick = trigger.nick
	else:
		nick = trigger.nick
	
	if nick:
		cur = con.cursor()
		cur.execute("SELECT u.nick, w.balance FROM user u, wallet w WHERE u.nick = '" + nick + "' AND w.id = u.btn_id")
		row = cur.fetchone()
		if row is None:
			bot.say(nick + " does not exist in the database.")
			return
		else:
			nick = str(row[0])
			balance = str(row[1])
			bot.say(nick + " has a balance of " + balance)
			return
		con.close()

@module.commands('credit')
def credit (bot, trigger):
	if trigger.group(3) and trigger.group(4):
		tnick, tamt = trigger.group(2).split(None, 1)
		nick = re.sub("[^a-zA-Z0-9]","", tnick)
		amt = re.sub("[^0-9]","", tamt)
	else:
		bot.say("Please enter in format of .credit <user> <amount>")
		return
	try:
		con = mdb.connect('localhost', 'casino', 'btncasino', 'casino');
	except:
		print "Error: Unable to connect to user settings DB."
		bot.say("Error: Unable to connect to DB.")
		return
	
	if nick and amt:
		cur = con.cursor()
		cur.execute("SELECT role FROM user WHERE nick = '" + trigger.nick + "';")
		row = cur.fetchone()
	if int(row[0]) >= staff:
		cur.execute("SELECT btn_id FROM user WHERE nick = '" + nick + "';")
		row = cur.fetchone()
		if row is None:
			bot.say(nick + " does not exist in the database.")
			return
		else:
			id = str(row[0])
			cur.execute("UPDATE wallet SET balance = balance + " + amt + " WHERE id = '" + id + "';")
			con.commit()
			cur.execute("SELECT balance FROM wallet WHERE id = '" + id + "';")
			row = cur.fetchone()
			balance = str(row[0])
			bot.say(amt + " credited into " + nick + "'s account. New balance: " + balance)
			return
		return
	else:
		bot.say("Please enter in format of .credit <user> <amount>")
		return
	con.close()	

@module.commands('debit')
def debit (bot, trigger):
	if trigger.group(3) and trigger.group(4):
		tnick, tamt = trigger.group(2).split(None, 1)
		nick = re.sub("[^a-zA-Z0-9]","", tnick)
		amt = re.sub("[^0-9]","", tamt)
	else:
		bot.say("Please enter in format of .debit <user> <amount>")
		return
	try:
		con = mdb.connect('localhost', 'casino', 'btncasino', 'casino');
	except:
		print "Error: Unable to connect to user settings DB."
		bot.say("Error: Unable to connect to DB.")
		return
	
	if nick and amt:
		cur = con.cursor()
		cur.execute("SELECT role FROM user WHERE nick = '" + trigger.nick + "';")
		row = cur.fetchone()
		if int(row[0]) >= staff:
			cur.execute("SELECT btn_id FROM user WHERE nick = '" + nick + "';")
			row = cur.fetchone()
			if row is None:
				bot.say(nick + " does not exist in the database.")
				return
			else:
				id = str(row[0])
				cur.execute("UPDATE wallet SET balance = balance - " + amt + " WHERE id = '" + id + "';")
				con.commit()
				cur.execute("SELECT balance FROM wallet WHERE id = '" + id + "';")
				row = cur.fetchone()
				balance = str(row[0])
				bot.say(amt + " debited from " + nick + "'s account. New balance: " + balance)
				return
			return
		else:
			bot.say("You do not have sufficient privileges.")
			return
	else:
		bot.say("Please enter in format of .debit <user> <amount>")
		return
	con.close()

@module.commands('newuser')
def newuser (bot, trigger):
	if trigger.group(3) and trigger.group(4) and trigger.group(5):
		tnick, tamt = trigger.group(2).split(None, 2)
		nick = re.sub("[^a-zA-Z0-9]","", tnick)
		amt = re.sub("[^0-9]","", tamt)
		id = re.sub("[^0-9]","", tid)
	else:
		bot.say("Please enter in format of .newuser <btn id> <user> <amount>")
		return
	try:
		con = mdb.connect('localhost', 'casino', 'btncasino', 'casino');
	except:
		print "Error: Unable to connect to user settings DB."
		bot.say("Error: Unable to connect to DB.")
		return
	
	if nick and amt and id:
		cur = con.cursor()
		cur.execute("SELECT role FROM user WHERE nick = '" + trigger.nick + "';")
		row = cur.fetchone()
		if int(row[0]) >= staff:
			cur.execute("INSERT INTO btn (btn_id, name) VALUES ('" + id + "', '" + nick + "');")
			cur.execute("INSERT INTO user (btn_id, nick, role) VALUES ('" + id + "', '" + nick + "', '1');")
			cur.execute("INSERT INTO wallet (id, balance) VALUES ('" + id + "', '" + amt + "');")
			con.commit()
			cur.execute("SELECT balance FROM wallet WHERE id = '" + id + "';")
			row = cur.fetchone()
			balance = str(row[0])
			bot.say("User: " + nick + "(" + id + ") created with a balance of " + amt)
			return
		else:
			bot.say("You do not have sufficient privileges.")
			return
	else:
		bot.say("Please enter in format of .newuser <btn id> <user> <amount>")
		return
	con.close()
