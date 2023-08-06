#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from multiprocessing import pool
#sys.path.append(__file__.replace("__init__.py",''))
imgpth=os.path.join( os.path.dirname(__file__),'images')
try:
	import gui
except:
	from . import gui

	
w=gui.window('Run to the hills')
w.win.update()
w.update(3)
try:
	import game
except:
	from . import game

w.update(20)
window = game.MyGame(os.path.join(imgpth,'Mountain_0sc.png'),w)
w.update(35)
window.start_new_game(20)
w.update(45)
game.arcade.run()