#!/usr/bin/env python
# -*- coding: utf-8 -*-

## SERGIO DEL CASTILLO t.me/sercliff

# FUTURE: Method of use of firebase
# firebase = pyrebase.initialize_app(auth.config())
# db = firebase.database()
# db.child("users").child("Morty").set(data) ## To create your own keys use the set() method. The key in the example below is "Morty".
# db.child("users").child("Morty").push(data) ## To save data with a unique, auto-generated, timestamp-based key, use the push() method.
# db.child("users").update(data) ## To update data for an existing entry use the update() method.
# db.child("users").remove(data) ## To delete data for an existing entry use the remove() method.

# user = db.child("users").get().key() ## Calling key() returns the key for the query data.
# user = db.child("users").get().val() ## Queries return a PyreResponse object. Calling val() on these objects returns the query data.
# all_users = db.child("users").get().each() ## Returns a list of objects on each of which you can call val() and key().
# for user in all_users:
#     print(user.key()) # Morty
#     print(user.val()) # {name": "Mortimer 'Morty' Smith"}

# user = db.child("users").get() ## To return data from a path simply call the get() method.


import auth
import pyrebase
import time
import hashlib

from aux import d2j
from aux import iprint
from aux import DEBUG
from aux import set_log as log


firebase = pyrebase.initialize_app(auth.config())
db = firebase.database()





def create_random_link(value):
	"""
	Create Random Link: Returns a link avaiable to your project
	-> return: new link of project 

	"""

	global db

	iprint (DEBUG.WARNING, "CREATING RANDOM LINK with: "+str(value))

	result = True
	while result != None:
		value = hashlib.md5(value.encode('utf-8')).hexdigest()
		result = db.child(str(value)).get().val()

	return value

	


def update_project(data):
	""" SAVE PROJECT """
	""" UPDATE PROJECT """

	iprint(DEBUG.WARNING, "SAVING DATA: "+ str(len(data)) +" projects")
	# iprint(DEBUG.PRINT, "DATA: "+str(data))
	#TODO: CREAR THREAD POOL PARA SUBIR TODOS LOS PROYECTOS MÁS RÁPIDO
	for project_id, project in data.items():

		
		iprint(DEBUG.WARNING, "SAVING DATA: "+ str(project_id)  +" project "+str(project))

		if 'project' in project:
			set_project_info(project_id, project['project'])

		if 'users' in project:
			for user_id, user_data in project['users'].items():
				set_collaborator(project_id, user_data)

		if 'files' in project:
			for file_name, files in project['files'].items():
				set_files(project_id, files)
			
		if 'file_data' in project:
			for file_name, file_data in project['file_data'].items():
				try:
					iprint(DEBUG.WARNING, "TRYING SAVE DATA AS DICT")
					for row, info in file_data.items():
						set_file_data(project_id, file_name, row, info)
				except Exception as e:
					iprint(DEBUG.WARNING, "DATA NOT SAVED AS DICT --> exception: "+str(e))
					iprint(DEBUG.WARNING, "TRYING SAVE DATA AS LIST")
					row = 0
					for info in file_data:
						if info != None:
							set_file_data(project_id, file_name, row, info)
						row+=1
		
	iprint(DEBUG.WARNING, "SAVED")


def set_project_info(project_id, project):
	""" Save Project Info """
	global db
	try:
		db.child(project_id).child("project").set(project)
	except Exception as e:
		iprint(DEBUG.ERROR, "[DataController][set_project_info]: Throw errors, exception: "+ str(e))


def set_files(project_id, files):
	""" Save Files Info of Project """
	global db
	try:
		db.child(project_id).child("files").child(hashlib.md5(str(files['name']).encode('utf-8')).hexdigest()).set(files)
	except Exception as e:
		iprint(DEBUG.ERROR, "[DataController][set_files]: Throw errors, exception: "+ str(e))


def set_file_data(project_id, file_name, row, row_data):
	""" Save row of file """
	global db
	try:
		db.child(project_id).child("file_data").child(str(file_name)).child(row).update(row_data)
	except Exception as e:
		iprint(DEBUG.ERROR, "[DataController][set_file_data]: Throw errors, exception: "+ str(e))


def set_collaborator(project_id, user_data):
	""" Save new collaborator of project """
	global db
	try:
		db.child(project_id).child("users").child(user_data['user_id']).set(user_data)
	except Exception as e:
		iprint(DEBUG.ERROR, "[DataController][set_collaborator]: Throw errors, exception: "+ str(e))


def delete_project(project_id):
	""" DELETE PROJECT """
	global db
	try:
		iprint (DEBUG.WARNING, "DELETING PROJECT ID ("+str(project_id)+")")
		db.remove(project_id)
		iprint (DEBUG.WARNING, "REMOVED")
	except Exception as e:
		iprint(DEBUG.ERROR, "[DataController][set_collaborator]: Throw errors, exception: "+ str(e))


def return_project(project_id):
	""" RETURN THE PROJECT IF EXISTS 
		-> Return a dict with all elements of project
	"""
	try:
		iprint (DEBUG.WARNING, "REQUEST OF PROJECT ("+str(project_id)+")")
		return db.child(project_id).get()
	except Exception as e:
		iprint(DEBUG.ERROR, "[DataController][return_project]: Throw errors, exception: "+ str(e))


def return_collaborators(project_id):
	""" RETURN THE COLLABORATORS OF A PROJECT IF IT HAVE 
		-> Return a dict with all collaborators of project
	"""
	try:
		iprint (DEBUG.WARNING, "REQUEST OF COLLABORATORS ("+str(project_id)+")")
		return db.child(project_id).child("users").get()
	except Exception as e:
		iprint(DEBUG.ERROR, "[DataController][return_project]: Throw errors, exception: "+ str(e))
























