import base64
import socket
import subprocess

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
      print 'Joined ' + channel
  
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
          print 'Connected and identified'
          break
  
  def mainloop(self):
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
          
          print '[' + sender + '] ' + msg
          
          if msg.count(' ') >= 2:
            # commands that take no args
            command = msg.split(' ')[1]
            
            if command == '$v8':
              if msg.split(' ')[2] == '--help':
                self.privmsg(to, 'Usage: ' + self.nick + ' $v8 [javascript]')
              else:
                # fucked up way to get the javascript
                javascript = msg[len(self.nick + command) + 2:].replace("\\r", '').replace("\\n", '').replace("\\", "\\\\").replace("\"", "\\\"")
                
                # insecure as fuck probably
                try:
                  # will be different depending on how you installed v8
                  self.privmsg(to, subprocess.check_output('v8 -e "' + javascript + '"', shell=True))
                except subprocess.CalledProcessError:
                  self.privmsg(to, 'There were errors in your script')
            
            if command == '$b64' and msg.count(' ') == 2:
              self.privmsg(to, 'Usage: ' + self.nick + ' $b64 --encode message')
              self.privmsg(to, '       ' + self.nick + ' $b64 --decode bWVzc2FnZQ==')
            
            if command == '$bin':
              try:
                self.privmsg(to, bin(int(msg.split(' ')[2])))
              except ValueError:
                self.privmsg(to, 'Invalid argument given')
            
            if command == '$hex':
              try:
                self.privmsg(to, hex(int(msg.split(' ')[2])))
              except ValueError:
                self.privmsg(to, 'Invalid argument given')
          
          if msg.count(' ') >= 3:
            if command == '$b64':
              flag = msg.split(' ')[2]
              text = msg[len(self.nick + command + flag) + 3:]
              print text
              if flag == '--encode':
                self.privmsg(to, base64.b64encode(text))
              elif flag == '--decode':
                self.privmsg(to, base64.b64decode(text))