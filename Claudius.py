import base64
import socket
import subprocess
import threading

class Claudius:
  def __init__(self):
    
    self.s = socket.socket()
    
    self.host = None
    self.port = None
    self.nick = None
    
    self.connected = False
  
  def setHost(self, host):
    self.host = host
  
  def setPort(self, port):
    self.port = port
  
  def setNick(self, nick):
    self.nick = nick
  
  def join(self, channel):
    if self.connected:
      self.s.send('JOIN ' + channel + "\r\n")
      print('Joined ' + channel)
  
  def privmsg(self, to, msg):
    if self.connected:
      self.s.send('PRIVMSG ' + to + ' :' + msg + "\r\n")
  
  def connect(self):
    if self.host != None and self.port != None and self.nick != None:
      self.s.connect((self.host, self.port))
      self.s.send('USER ' + self.nick + ' 0 * :' + self.nick + "\r\n")
      self.s.send('NICK ' + self.nick + "\r\n")
      
      # try to join chans and get the hell outta there
      while 1:
        data = self.s.recv(512)
        if data[0:4] == 'PING':
          self.s.send(data.replace('PING', 'PONG'))
        if data[0]!=':':
          continue
        if data.split(' ')[1] == '001':
          self.s.send('MODE ' + self.nick + " +B\r\n")
          self.connected = True
          print('Connected and identified')
          break
  
  def start(self):
    if self.connected:
      while 1:
        data = self.s.recv(512)
        if data[0:4] == 'PING':
          self.s.send(data.replace('PING', 'PONG'))
        elif data[0]!=':':
          continue
        elif data.split(' ')[1] == 'PRIVMSG' and data.split(':')[2].startswith(self.nick):
          rcpt   = data.split(' ')[2]
          sender = data[1:].split('!')[0]
          to     = sender
          
          # make sure we don't send the reply to the bot..
          if rcpt != self.nick:
            to = rcpt
          
          # fucked up way to get the message
          msg = data[data.index(':', 1):].strip()[1:]
          
          print('[' + sender + '] ' + msg)
          
          Parse(self, msg, to).start()

class Parse(threading.Thread):
  def __init__(self, claudius, msg, to):
    threading.Thread.__init__(self)
    self.claudius = claudius
    self.msg = msg
    self.to = to
  
  def run(self):
    if self.msg.count(' ') >= 2:
      # commands that take no args
      command = self.msg.split(' ')[1]
      
      if command == '$v8':
        if self.msg.split(' ')[2] == '--help':
          self.claudius.privmsg(to, 'Usage: ' + self.claudius.nick + ' $v8 [javascript]')
        else:
          # fucked up way to get the javascript
          javascript = self.msg[len(self.claudius.nick + command) + 2:].replace("\\", "\\\\").replace("\"", "\\\"").replace("$", "\$")
          
          # insecure as fuck probably
          try:
            # will be different depending on how you installed v8
            self.claudius.privmsg(self.to, subprocess.check_output('v8 -e "' + javascript + '"', shell=True).replace("\r", '').replace("\n", ''))
          except subprocess.CalledProcessError:
            self.claudius.privmsg(self.to, 'There were errors in your script')
      
      if command == '$b64' and msg.count(' ') == 2:
        self.claudius.privmsg(self.to, 'Usage: ' + self.claudius.nick + ' $b64 --encode message')
        self.claudius.privmsg(self.to, '       ' + self.claudius.nick + ' $b64 --decode bWVzc2FnZQ==')
      
      if command == '$bin':
        try:
          self.claudius.privmsg(self.to, bin(int(msg.split(' ')[2])))
        except ValueError:
          self.claudius.privmsg(self.to, 'Invalid argument given')
      
      if command == '$hex':
        try:
          self.claudius.privmsg(self.to, hex(int(msg.split(' ')[2])))
        except ValueError:
          self.claudius.privmsg(self.to, 'Invalid argument given')
    
    if self.msg.count(' ') >= 3:
      if command == '$b64':
        flag = self.msg.split(' ')[2]
        text = self.msg[len(self.claudius.nick + command + flag) + 3:]
        if flag == '--encode':
          self.claudius.privmsg(to, base64.b64encode(text))
        elif flag == '--decode':
          self.claudius.privmsg(to, base64.b64decode(text))
