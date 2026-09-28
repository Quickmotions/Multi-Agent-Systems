import numpy as np

import asyncio
import random
import uuid
won = False
winner = None
turn = 0
board = [ ’ - ’ ]*9

class Agent () :
    def __init__ ( self , player ) :
    self . alive = True
    self . uid = uuid . uuid4 ()
    self . player = player

    def act ( self ) :
    unplayed = []
for x in range (9) :
if board [ x ] == ’ - ’:
unplayed . append ( x )
pos = random . choice ( unplayed ) board [ pos ] = self . player
25
26 async def run ( self ) :
while True :
    self.act ()
    environment ()
    try :

    await asyncio.sleep(1)
except asyncio.Cancelled Error as e:
    print("Stopping agents & cleaningup... " )
    raise