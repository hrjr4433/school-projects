#!/usr/bin/python
#############################################################################
# Program:
#    Final project, Computer Communication and Networking
#    Brother Jones, CS 460
# Author:
#    Jay Lee
# Summary:
#    1. Real Time Boxing game client
#    2. It first creates connection with server
#    3. Then wait for opponent
#    3. When the game begins create 'select'
#    5. It handles user inputs and server inputs
#    6. Allowed command 'a', 's', 'd'
#    7. If there is input from server side = command processed on server side
#    8. Then reset the command to '.'
#    9. It display commands of the player and the opponent and remaining HP
#   10. It shows if you win, lose, draw from command 'l', 'w', and 'd'
#   11. It also can handle 'c' command which closed connection
#   12. It close connection and exit program when the game is over
#############################################################################
from socket import *
import os
import time
import select 
import socket 
import sys
  
#############################################################################
# command evaluation. 'a'(left), 's'(block), 'd'(right), and '.' (blank)
#############################################################################
def evaluate_cmd(cmd):
  if (cmd in ('a', 's', 'd', '.')):
    return True
  else:
    return False
    
#############################################################################
# process command from server
# it shows yours and opponent's commands with your remaining HP
#############################################################################
def command_processor(server_cmd):
  if (server_cmd in ('l', 'w', 'd')):
    print '\rGame Over!                            '
    if (server_cmd == 'l'):
      print 'You Lose!'
    elif (server_cmd == 'd'):
      print 'Cross Counter! Draw!'
    else:
      print 'You Win!'
    return True
  else:
    server_cmds = server_cmd.split(' ')
    if (evaluate_cmd(server_cmds[0]) & evaluate_cmd(server_cmds[1])):
      sys.stdout.write('\rYour command: ' + server_cmds[0] + ' Opponent\'s command: ' + server_cmds[1] + ' remained HP: ' + server_cmds[2] + ' ')
      sys.stdout.flush()
    return False
  
################################### main ####################################
print 'Welcome to real time boxing game\n'
name = raw_input('Please, enter your name: ')
host = gethostname()
server_host = raw_input('Host: ')
server_port = input('Port: ')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket
server.bind((host, server_port)) # bind
server.connect((server_host, server_port)) # connect
print 'Connecting to server...'
server.send(name) # sending player name
while True:
  serverInfo = server.recv(1024) # getting wait, ready
  if (serverInfo <> ''):
    print serverInfo    
  if (serverInfo == 'opponent is ready'):
    break
  serverInfo = ''

opponent_name = server.recv(1024) # getting the name of the opponent

# showing a picture. supposed to be a pair of boxing gloves
print '         ||   ||           '
print '         ||   ||           '
print '         ||   ||           '
print '      ___||___||____       '
print '    _| _______  |__ |__    '
print '    | |       |    \   \   '
print '    | | R.T.B |     \   \   '
print '    | |_______|     /   /   '
print '    |            \_/  _/   '
print '     \             \  \    '
print '       \___________/__/    '

# showing the name of the opponent, commands can be used
print 'Your opponent is ' + opponent_name
print 'Command = a(left),s(block),d(right) + enter'
time.sleep(2)
print 'ready? hit command + enter!'
time.sleep(0.5)

# select make the program able to handle multiple input
try:
  while True:
    input = [server, sys.stdin]
    inputready,outputready,exceptready = select.select(input,[],[])
    os.system("stty -echo") # no echo of input
    for s in inputready:
      if s == server:
        server_cmd = server.recv(1024)
        if (server_cmd == 'c'):
          server.close
          sys.exit(0)
        if (command_processor(server_cmd)):
          break
        server.send('.')
      elif s == sys.stdin:
        to_server = sys.stdin.read(1)
        if evaluate_cmd(to_server):
          server.send(to_server)
except KeyboardInterrupt:
  os.system("stty echo") # back to input with echo
  server.send('c')
  server.close()
finally:
  os.system("stty echo") # back to input with echo
  server.close()
  print "\nClosing Game"
