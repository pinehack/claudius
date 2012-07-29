from Claudius import *


bot = Claudius()
bot.setHost('irc.foonetic.net')
bot.setPort(7000) # it's less than 9000..
bot.setNick('claudius')
bot.connect()

bot.join('#jakash3')

bot.start()