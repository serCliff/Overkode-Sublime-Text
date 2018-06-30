#!/usr/bin/env python
# -*- coding: utf-8 -*-

## SERGIO DEL CASTILLO t.me/sercliff




import auth
import pyrebase
import time
import json
import hashlib
import os
import glob
import threading

import Project
import DataController as dc
import UpdatesController

from aux import d2j
from aux import iprint
from aux import DEBUG
from aux import set_log as log



class ProjectController:

	def __init__(self, owner_id, collaborators, project_id, link, platform):
		self.owner_id = owner_id
		self.project_id = project_id
		self.link = link
		self.platform = platform
		self.updates_controller = None

		## FUTURE: En colaboradores incluir en primer momento el owner(unico usuario e ir añadiendole el resto)
		## FUTURE: Collaborators solo sirve en caso de querer incluir varios usuarios desde un primer momento pero no tiene que ser una funcionalidad necesaria
		self.collaborators = collaborators 

	def new_project(self, scope, permissions):
		""" 
			MAKE A NEW PROJECT AND SAVE IN THE DATABASE 
			:param scope       : Determine the range of work, Project or file, and where are all
			:param permissions : Determine the permissions of all project (For partial sharing in selected_text() method)
									- Read: Can be only read or some rows will be changed in the future with selected_text()
									- Write: All permissions to make changes
									- NONE: None will be readed or writed, needed selected_text() for special row permissions
			
			-> Return   : Link/id of the project 
		"""

		## TODO: Controlar gitignore
		general_permissions = dict()

		#TODO: Por defecto los permisos serán los establecidos al crear el PC obtenidos de permissions y modificarán el comportamiento 
		# 		de la lectura de ficheros puesto que no hará falta subir lo que no se utilice o se podrá subir después
		print("Permisos: "+str(permissions.value)+" - "+str(Project.Permissions.READ.value))
		general_permissions['general'] = Project.Permissions.READ.value  ## By default the permissions of files will be READ
		if permissions.value == Project.Project_Permissions.FULL.value:
			general_permissions['general'] = Project.Permissions.WRITE.value
			#TODO: ELiminar comentario después de comprobar
			print("Permisos generales establecidos a escritura")
		
		time.sleep(10)
		

		current_directory = os.getcwd()+"/"	
		
		if self.platform != "web":

			if 'range' in scope and scope['range'] == "project": ## We are sharing all our project
				## MAKING FULL PROJECT WITH ALL PROJECT	
				#FUTURE: Para que solo algún archivo del proyecto se pueda editar y el resto visualizar, utilizar el método selected_text()

				all_files = glob.glob(current_directory+'**', recursive=True) ## This version return an iterator, glob.glob returns a list 
				all_files.remove(os.getcwd()+"/")
				
				iprint (DEBUG.PRINT, current_directory)

				# iprint (DEBUG.PRINT, "\n|\t\tDIRECTORIES\r\t\t\t\t\t|\t\tDIRECTORY")
				# for file in all_files:
				# 	if os.path.isdir(file):
				# 		iprint (DEBUG.PRINT, "| "+os.path.basename(file)+"\r\t\t\t\t\t| "+file.replace(current_directory, "/"))


				
				# TODO: Estudiar hacer ambos tipos con un único controlador, "proyectos" de un sólo archivo
				# iprint (DEBUG.PRINT, "\n|\t\tFILE\r\t\t\t\t\t|\t\tDIRECTORY")
				files = dict()
				for file in all_files:
					if os.path.isfile(file):
						iprint (DEBUG.PRINT, "| "+os.path.basename(file)+"\r\t\t\t\t\t| "+file.replace(current_directory, "/"))

						name = str(os.path.basename(file))
						path = file.replace(current_directory, "/")
						
						iprint (DEBUG.PRINT, "| "+name+"\r\t\t\t\t\t| "+path)
						row_info = create_project_rowInfo(file, general_permissions) ## GENERAL PERMISSIONS EXPLAINED ON THE METHOD
						file = create_project_files(name, path, permissions.value, row_info)
						name_id = hashlib.md5(name.encode("utf-8")).hexdigest()
						files[name_id] = file
				
				project = dict()
				project[self.project_id] = create_project(self.project_id, self.link, permissions.value, self.owner_id, files, self.collaborators)
				# dc.update_project(project_to_json(project))
				dc.update_project(d2j(project))
				

				self.updates_controller = UpdatesController.UpdatesController(self.project_id, self.owner_id)
				begin_updates(self.updates_controller)






			elif 'range' in scope and scope['range'] == "file": ## Only we will share the file with name is in scope['path']
				## MAKING FULL PROJECT WITH ONE FILE
				file = scope['path']
				name = str(os.path.basename(file))
				path = file.replace(current_directory, "/")
				
				iprint (DEBUG.PRINT, "| "+name+"\r\t\t\t\t\t| "+path)
				row_info = create_project_rowInfo(file, general_permissions)
				file = create_project_files(name, path, permissions.value, row_info)
				files = dict()
				name_id = hashlib.md5(name.encode("utf-8")).hexdigest()
				files[name_id] = file

				project = dict()
				project[self.project_id] = create_project(self.project_id, self.link, permissions.value, self.owner_id, files, self.collaborators)
				# dc.update_project(project_to_json(project))
				dc.update_project(d2j(project))


				self.updates_controller = UpdatesController.UpdatesController(self.project_id, self.owner_id)
				begin_updates(self.updates_controller)
				
				
				#TODO: CREAR SISTEMA DE SOPORTE PARA ARCHIVOS BINARIOS, FOTOGRAFÍAS, ETC

		else: 
			iprint(DEBUG.PRINT, "With web platform create a new file of project and begin")
			# TODO: CREAR LO NECESARIO PARA PLATAFORMA WEB

	def add_collaborator(user_id, project_id):
		""" Add a collaborator """
		iprint (DEBUG.PRINT, "NEW COLLABORATOR")
		self.updates_controller = UpdatesController.UpdatesController(self.project_id, self.owner_id)
		begin_updates(self.updates_controller)

	def show_project_id(self):
		#TODO: show_project_id, crear método que represente esta información en el plugin
		return self.link

	def stop_streaming(self):
		stop_updates(self.updates_controller)


	def selected_text(self, file_id, permissions):
		""" Set permissions for determined rows of the file 
			:param file_id 		: hash of file to make special permissions
			:param permissions 	:
		"""
		#TODO: selected_text
		iprint (DEBUG.PRINT, "Making special permissions for selected file")




	def change_permissions(self, permissions):
		#TODO: change_permissions
		""" Mostrar permisos, decir a que pueden cambiar y cambiar """
		iprint (DEBUG.PRINT, "something")





## ············································································································································ ##


def test_update(project_id, owner_id):
	updates_controller = UpdatesController.UpdatesController(project_id, owner_id)
	begin_updates(updates_controller)
	

def begin_updates(updates_controller):
	""" PROCESS TO MANAGE UPDATES TO A USER """

	iprint(DEBUG.WARNING, "Starting streaming updates")
	t = threading.Thread(target=updates_controller.receive_updates)
	# t = threading.Thread(target=u.updates, args=("mugreee",))
	t.start()


def stop_updates(updates_controller):
	""" FINISHING STREAMING UPDATES """
	
	iprint(DEBUG.WARNING, "Finishing updates")
	updates_controller.stop_updates()
	iprint(DEBUG.WARNING, "Finished")



def create_project(project_id, link, permissions, owner_id, files, users):
	""" Makes the json with the data of the files passed by arguments
		
		:param project_id 	: Id of the project
		:param link 		: Link of the project
		:param permissions 	: dict[row, permission]
		:param owner_id 	: Id of the owner of the project
		:param files 		: List of files to be included on the project
		:param users 		: List of collaborators
	"""
	
	project = dict()
	project_data = dict()
	project_data["id"] = project_id
	project_data["permissions"] = permissions
	project_data["link"] = link
	project_data["owner_id"] = owner_id
	project["project"] = project_data

	file_files = dict()
	file_data = dict()
	for key, data in files.items():
		file_files[key] = data["files"]
		file_data[key] = data["file_data"]

	project["files"] = file_files
	project["file_data"] = file_data

	project["users"] = users
	return project

def create_user(user_id, name, platform):

	user = dict()
	user["user_id"] = user_id
	user["name"] = name
	user["platform"] = platform
	return user
	
	


def create_project_files(name, path, permissions, data):
	# return Project.Files(name, path, permissions, data)
	iprint (DEBUG.PRINT, "CREATING PROJECT FILE INFO")
	project_files = dict()
	project_data = dict()
	project_data["name"] = name
	project_data["path"] = path
	project_data["permissions"] = permissions
	
	project_files["files"] = project_data
	project_files["file_data"] = data
	
	return project_files


def create_project_rowInfo(file_path, permissions):
	""" 
		Make a RowInfo class with the information content in the file 
		:param file_path   : The path of file that will be readed
		:param permissions : dict[row, permission] with special permissions (if is empty all rows have Permissions.WRITE) || 'general' to assign manually general permissions
		-> Return   : dict[row, RowInfo] filled with the file_path information
	"""
	iprint (DEBUG.WARNING, "CREATING PROJECT RowInfo to: "+str(file_path))

	row_info = dict()
	row_json = dict()
	try:
		timestamp = "00/00/0000"
		
		if len(permissions):
			row_permissions = Project.Permissions.READ.value
		elif 'general' in permissions:
			row_permissions = permissions['general']
		else:
			row_permissions = Project.Permissions.WRITE.value
		
		try:
			with open(file_path) as file:
				row=1
				for line in file:
					rowinfo_json = dict()
					rowinfo_json["text"] = line
					rowinfo_json["permissions"] = row_permissions
					rowinfo_json["timestamp"] = timestamp
					row_json[row] = rowinfo_json
					del rowinfo_json
					row+=1

					#Antiguo sistema con clases
					# row_info[row] = Project.RowInfo(line, row_permissions, timestamp)

			# print("\nrow_json")
			# print(row_json)
			# print("\nrow_json[1]")
			# print(row_json[1])
			# print("\nrow_json[1][text]")
			# print(row_json[80]["text"])


			try:
				# Change to write the needed rows
				#TODO: Repasar, si utilizamos un sistema con jsons es necesario cambiar row_info por row_json y modificar los permisos
				if not 'general' in permissions and len(permissions):
					iprint(DEBUG.PRINT, "Rewrite rows with special permissions")
					for row, permission in permissions.items():
						row_info[row].set_permissions(permission)



			except Exception as e:
				iprint(DEBUG.ERROR, "[ProjectController][create_project_rowInfo] : Changing File Permissions was thrown an exception: "+str(e))
		
		except Exception as e: 	##---------------> TO BINARY FILES	
			#TODO: Mirar como solucionar el asunto para archivos que no son legibles
			#TODO: Evitar almacenar información de archivos de los que no tenemos datos almacenados
			iprint(DEBUG.WARNING, "---------------> THATS A BINARY FILE")
			# with open(file_path, "rb") as file:  
		
	except Exception as e:
		iprint(DEBUG.ERROR, "[ProjectController][create_project_rowInfo] : Reading File was thrown an exception: "+str(e))


	iprint(DEBUG.WARNING, "RowInfo was done\n")

	return row_json
	# return row_info








# DEPRECATED ¿?
def project_to_json(project):

	""" Change project created on classes to JSON to be saved 
		-> Return a json with all elements of project
	"""

	iprint (DEBUG.PRINT, "***************************")
	iprint (DEBUG.PRINT, "PARSE PROJECT TO JSON\n")

	projects = dict()


	project_data = dict()
	project_data["id"] = project.get_project_id()
	project_data["permissions"] = project.get_permissions()
	project_data["link"] = project.get_link()
	project_data["owner_id"] = project.get_owner_id()
	
	files = dict()
	file_data = dict()
	for name, file in project.get_files().items():
		
		name = hashlib.md5(name.encode('utf-8')).hexdigest()
		
		files[name] = dict()
		files[name]["name"] = file.get_name()
		files[name]["path"] = file.get_path()
		files[name]["permissions"] = file.get_name()

		file_data[name] = dict()
		for row, row_data in file.get_data().items():
			file_data[name][row] = dict()
			file_data[name][row]["text"] = row_data.get_text()
			file_data[name][row]["permissions"] = row_data.get_permissions()
			file_data[name][row]["timestamp"] = row_data.get_timestamp()
			del row_data
		del file

	users = dict()
	for user_id, user in project.get_users().items():
		users[user_id] = dict()
		users[user_id]["name"] = user.get_name()
		users[user_id]["platform"] = user.get_platform()
		users[user_id]["user_id"] = user.get_user_id()
		del user
	del project
	# iprint (DEBUG.PRINT, "")

	item = dict()
	item["project"] = project_data
	item["files"] = files
	item["file_data"] = file_data
	item["users"] = users

	projects[project_data["id"]] = item

	# iprint (DEBUG.PRINT, projects)
	returned_data = json.dumps(projects)
	data_string = json.dumps(projects, sort_keys=True, indent=4, separators=(',', ': '))
	
	iprint (DEBUG.PRINT, 'JSON:'+ str(data_string))

	# return returned_data
	return json.loads(returned_data)

