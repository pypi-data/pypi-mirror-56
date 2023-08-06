#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from multiprocessing import pool
import time
class window:
	def __init__(self,title,iconpath=None,height=200,width=400):
		self.win= tk.Tk()
		self.win.title(title)
		self.win.geometry('%sx%s' %(width,height))
		if not iconpath=='':
			self.win.iconbitmap(iconpath)
			
		self.label=tk.StringVar(self.win)
		label=tk.Label(self.win,textvariable=self.label)
		self.label.set("Please wait while the game loads")
		label.place(x=20, y=30,in_=self.win)
		
		
		self.progressbar=ttk.Progressbar(self.win,orient=tk.HORIZONTAL,length=200,mode='determinate')
		self.progressbar.place(x=50, y=100,in_=self.win)
		
		
		self.win.attributes('-topmost', True)




	def close(self):
		self.win.destroy()
		
	def update(self,value):
		self.progressbar['value']=value
		self.win.update_idletasks()		
		



