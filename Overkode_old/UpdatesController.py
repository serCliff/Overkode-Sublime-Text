#!/usr/bin/env python
# -*- coding: utf-8 -*-

## SERGIO DEL CASTILLO t.me/sercliff



import auth
import pyrebase
import time
import json
import Project
import hashlib
import os
import glob
import threading

import sys


import DataController as dc

from aux import d2j
from aux import iprint
from aux import pretty
from aux import DEBUG
from aux import set_log as log



firebase = pyrebase.initialize_app(auth.config())
db = firebase.database()



def stream_handler(message):
	""" 
		Here comes all information thats was edited on the stream
		
		Still missing sublime and web modules to represent the information obtained here on the different editors

	"""
	#TODO: Crear un hilo por cada fichero (pool con varios) editado recibido para mejorar el rendimiento
	#TODO: No mandarle al usuario lo que cambie el
	
	project_id = str(message["stream_id"])
	try:
		update = dict()
		update[project_id] = recursive_structure(str(message["path"]), message["data"])
		print (pretty(update))
		#TODO: Crear sistema para representar la información en el editor

	except Exception as e:
		a = 0
	

def recursive_structure(path_data, data):
	""" Make recursively the project data 
		
		It makes the correct json to save the information on the correct file, row...
	"""
	
	key = os.path.basename(path_data)
	
	new_data = dict()
	new_data[key] = data

	new_path = path_data.replace("/"+str(key), "")
	
	if new_path == "" or path_data == "/":
		return new_data
	else:
		return recursive_structure(new_path, new_data)
	


class UpdatesController:

	def __init__(self, project, user_id):
		self.project = project
		self.user_id = user_id
		self.stream = None


	def receive_updates(self):
		global db

		print("thread working in stream: "+str(self.project)+" and user_id: "+str(self.user_id))

		try:
			self.stream = db.child(self.project).stream(stream_handler, stream_id=self.project)
		except KeyboardInterrupt:
		    self.stream.close()
		    sys.exit()




	def stop_updates(self):
		self.stream.close()











