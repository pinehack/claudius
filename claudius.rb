require "socket"

server = "irc.foonetic.net"
port = "6667"
nick = "Claudius"
owner = "PineHack"
channels = ["#jakash3", "#pinehack"]

s = TCPSocket.open(server, port);
s.puts "USER #{nick} 0 * :#{owner}"
s.puts "NICK #{nick}"

until s.eof? do
  data = s.gets

  if data.start_with?("PING")
    s.puts "PONG " +  data.split()[1]
  elsif data.split(" ")[1].start_with?("001")
    s.puts "MODE #{nick} +B"
    channels.each {|channel| s.puts "JOIN #{channel}"}
    
  elsif data.split(' ')[1] == 'PRIVMSG'
    if data.split(' ')[2] == nick
      puts '-' + data.split('!')[0].split(':')[1] + '!' + data.split(' ')[2] + '- ' + data.split(':')[2]
    else
      puts '-' + data.split('!')[0].split(':')[1] + data.split(' ')[2] + '- ' + data.split(':')[2]
    end

  elsif data.split(' ')[1] == 'NOTICE'
    if data.split(' ')[2] == nick
      puts '*' + data.split('!')[0].split(':')[1] + '!' + data.split(' ')[2] + '* ' + data.split(':')[2]
    else
      puts '*' + data.split('!')[0].split(':')[1] + data.split(' ')[2] + '* ' + data.split(':')[2]
    end
  end
    
end