from willie import module

game = 0
sw = ''
gm = ''

@module.rule('')
def swwin (bot, trigger):
	global game, sw, gm
	if game==1:
		t0 = trigger
		if sw in t0.lower() and trigger.nick != gm:	
			bot.say(trigger.nick + " won the secret word game. The word was " + sw + ".")
			game = 0
			return
		return

@module.commands('setword')
def setsw (bot, trigger):
	global game, sw, gm
	if game==0:
		sw = trigger.group(2)
		gm = trigger.nick
		game = 1
		bot.say("Secret word set as " + sw)
		return
	else:
		bot.say("There is already a game going on. The word is " + sw + ".")
		return

@module.commands('swstop')
def swstop (bot, trigger):
	global game, sw, gm
	if game ==1:
		bot.say(trigger.nick + " has stopped the secret word game started by " + gm + ".")
		game = 0
		sw = 0
		gm = 0
		return