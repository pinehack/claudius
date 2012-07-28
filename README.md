# claudius
claudius is an OOP irc bot written in python

## commands
 - `$b64 [--encode | --decode] [message]` - encodes/decodes base64
 - `$bin [input]` - translates integers to binary
 - `$hex [input]` - translates integers to hex
 - `$v8 [javascript]` returns javascript output (removes `\r` & `\n` for
   security purposes) you have to install v8 on your computer and create a
   symlink to the v8 example shell that is within your shell's path named v8

## application
This bot may not have much functionality, but the ability to interpret
javascript is unique enough to make this bot robust. Since several javascript
statements can be written on one line, you can get an enourmous amount of use
from this simple feature.

For instance, if I wanted to have a decision decided for me, I could execute
the following
```
claudius $v8 if(Math.random() < 0.5){ print("option one"); } else {
print("option two"); }
```
and from that, claudius would either print `option one` or `option two`.