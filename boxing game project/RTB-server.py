#!/usr/bin/python
#############################################################################
# Program:
#    Final project, Computer Communication and Networking
#    Brother Jones, CS 460
# Author:
#    Jay Lee
# Summary:
#    1. Real Time Boxing game server
#    2. It opens a socket and takes two clients
#    3. It sends welcome messages and ready messages to clients
#    4. It's using select to handle client's input and server side input
#    5. It's using thread to run the game (damage calculation)
#    6. 's' or same command will result damage 0
#    7. 'a' or 'd' will cause damage 10
#    8. It sends out win, draw, lose command when either one of HP is 0
#    9. 'c' means closed, it send other client win command
#   10. 't' or ctr + c will close the server and send out 'c' to clients
#############################################################################
from socket import *
import socket 
import select
import sys
import threading
import time

#############################################################################
# a class handle the game(damage calculation) with threading
#############################################################################
class Threaded_game(threading.Thread):  
  ###########################################################################
  # calculate the damage
  ###########################################################################
  def process_commands(self, command1, command2):
    damage = 0
    if (command1 == 's' or command1 == command2):
      damage = 0
    elif (command2 in ('a','d')):
      damage = 10
    return damage
  
  ###########################################################################
  # call process_commands and send out messages 
  ###########################################################################
  def damage_calculation(self):
    global hp1
    global hp2
    global client1cmd
    global client2cmd
    global client1
    global client2
    global running
    global server_command
    
    # server or client closed case
    if (client1cmd == 'c' or client2cmd == 'c' or server_command == 't'):
      return True
    
    # damage calculation
    hp1 -= self.process_commands(client1cmd, client2cmd)
    hp2 -= self.process_commands(client2cmd, client1cmd)
    
    # remaining HPs
    currently = '\rplayer1: ' + str(hp1) + ' player2: ' + str(hp2) + '   '
    sys.stdout.write(currently)
    sys.stdout.flush()
    
    # send out messages
    client1.send(client1cmd + ' ' + client2cmd + ' ' + str(hp1))
    client2.send(client2cmd + ' ' + client1cmd + ' ' + str(hp2))
    time.sleep(0.05)
    # win, lose, and draw
    if (hp1 <= 0 or hp2 <= 0):
      if (hp1 == 0 and hp2 == 0):
        client1.send('d')
        client2.send('d')
      elif (hp1 == 0):
        client2.send('w')
        client1.send('l')
      elif (hp2 == 0):
        client1.send('w')
        client2.send('l')
      running = 0
      return True
    else:
      return False
  
  ###########################################################################
  # run function calls damage calculation
  # it can break out the loop by win, lose, termination, or iteration
  ###########################################################################
  def run(self):
    iteration = 0
    while (iteration < 120):
      time.sleep(0.5)
      if (self.damage_calculation()):
        break
      iteration += 1
    self.exit()
      
  ###########################################################################
  # terminates thread
  ###########################################################################
  def exit(self):
    if self.isAlive():
      try:
        self._Thread__stop()
        print '\nGame Over'
      except:
        print(str(slef.getName())) + ' could not be terminated'

################################ main #######################################
print 'Welcome to real time boxing server\n'
port = input('Port number: ')
host = gethostname()
print 'the host is ' + host
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket
server.bind((host, port)) # bind
server.listen(5) # 5 = backlog

try:
  while True:
    (client1, address1) = server.accept() # client 1
    print 'Peer 1 has connected from ' + address1[0]
    client1name = client1.recv(1024)
    client1.send('server connected')
    client1.send('waiting for opponent')
    (client2, address2) = server.accept() # client 2
    print 'Peer 2 has connected from ' + address2[0]
    client2name = client2.recv(1024)
    client2.send('server connected')
    # sends out ready message
    client1.send('opponent is ready')
    time.sleep(0.05)
    client1.send(client2name)
    client2.send('opponent is ready')
    time.sleep(0.05)
    client2.send(client1name)

    # game settings
    print 'the termination command is \'t\''
    thread = Threaded_game(name = "Thread-1")
    hp1 = 100
    hp2 = 100
    client1cmd = '.'
    client2cmd = '.'
    running = 1
    thread.start()
    server_command = ''
    
    # select make the program able to handle multiple input
    while running:
      input = [client1, client2, sys.stdin]
      i,o,e = select.select(input,[],[], 1)
      for s in i:
        if s == client1:
          client1cmd = client1.recv(1) # command = a char
        elif s == client2:
          client2cmd = client2.recv(1) # command = a char
        elif s == sys.stdin:
          server_command = sys.stdin.read(1)
          if (server_command == 't'): # termination
            running = 0
      if (client1cmd == 'c'): # client closed
        client2.send('w')
        running = 0
      elif (client2cmd == 'c'):
        client1.send('w')
        running = 0
    
    time.sleep(1)
    if (client1cmd <> 'c'):
      client1.send('c')
    if (client2cmd <> 'c'):
      client2.send('c')
    client1.close()
    client2.close()
    if (server_command == 't'):
      break
      
except KeyboardInterrupt:
  running = 0
  client1.send('c')
  client2.send('c')
  thread.exit()
finally:
  server.close()
  print "\nClosing Server"