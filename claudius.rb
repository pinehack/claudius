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

  elsif ['PRIVMSG', 'NOTICE'].include?(data.split(' ')[1])
    from = data.split('!')[0].split(':')[1]
    rcpt = data.split(' ')[2]
    body = data.split(':')[2]
    type = data.split(' ')[1]
    char = '-'
    if type == 'NOTICE' char = '*'
    if rcpt == nick
      puts char + from + '!' + rcpt + char + ' ' + body
    else
      puts char + from + rcpt + char + ' ' + body
    end
  end
end