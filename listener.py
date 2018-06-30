#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
# from .sample.main import main as test
import sys


from .tornado import websocket
# import six
# from .websocket import create_connection
# from .sample.main import main as test




class EchoWebSocket(websocket.WebSocketHandler):
      def open(self):
          print ("WebSocket opened")

      def on_message(self, message):
          self.write_message(u"You said: " + message)

      def on_close(self):
          print ("WebSocket closed")

# import pyrebase

# https://stackoverflow.com/questions/15180537/how-to-include-third-party-python-packages-in-sublime-text-2-plugins?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

# import pyrebase
# from .Overkode.overkode import DataController
# https://trello.com/b/bngZbCrY/overkode


class ListenerClass(sublime_plugin.EventListener):
    
    def __init__(self):
        self.files = dict()
        self.project = dict()
        self.current_counter = 0
        self.document_size = 0
        self.last_document_size = 0
        self.total_rows = 0
        self.last_total_rows = 0


    def set_current_values(self, view):
        """ 
        Update de mantaining values to make only the needed updates 

        """
        # for i in sys.path:
        #   print (i)

        file = self.files[view.file_name()]

        if file.document_size == 0 and file.last_document_size == 0 :
            file.last_document_size = view.size()
            file.document_size = view.size()

        # SET INITIAL DOCUMENT COUNTER
        if file.current_counter == 0:
            file.current_counter = view.change_count()

        # SET INITIAL DOCUMENT ROWS
        current_rows = len(view.split_by_newlines(sublime.Region(0, view.size())))
        if file.total_rows == 0 and file.last_total_rows == 0:
            file.last_total_rows = current_rows
            file.total_rows = current_rows



        # MANTAIN CURRENT VIEW SIZE UPDATED
        if file.document_size != view.size():
            file.last_document_size = file.document_size
            file.document_size = view.size()

        # print(str(file.last_total_rows)+" = "+str(file.total_rows)+" = "+str(current_rows))   
        file.last_total_rows = file.total_rows
        file.total_rows = current_rows




    def on_selection_modified(self, view):
        # print("El file_name es: "+str(view.file_name()))
        # w = view.window()
        # print(w.extract_variables())
        # p = w.active_sheet()
        # print(p)

        # visible_region = view.visible_region()
        # print(visible_region)
        fname = view.file_name()
        if not fname in self.files:
            # print (fname)
            self.files[fname] = OverkodeFileData(str(fname).replace(" ","\ "))
        file = self.files[fname]


        file_reg = sublime.Region(0, view.size())
        # print(file_reg)
        # print(len(view.split_by_newlines(file_reg)))

        # print(view.substr(region))

        print(sys.path)
        # print(create_connection("ws://localhost:8080/websocket"))


        self.set_current_values(view)

            # print(view.full_line(i))
        if file.current_counter != view.change_count():
            file.current_counter = view.change_count()

            # print(view.sel()[0].begin())
            for pos in view.sel():
                index=0
                for i in view.split_by_newlines(file_reg):
                    index+=1
                    if pos.begin() >= i.begin() and pos.begin() <= i.end():
                        
                        #FUTURE: Add text into a row
                        if file.last_total_rows == file.total_rows:
                            print("["+str(index)+"] ("+str(i.begin())+", "+str(i.end())+"): "+view.substr(i))
                            


    def on_post_text_command(self, view, command_name, args):
        print(command_name)
        
        if command_name == "duplicate_line":
            print(view.sel()[0].begin())
            for pos in view.sel():
                index=0
                for i in view.split_by_newlines(sublime.Region(0, view.size())):
                    index+=1
                    if pos.begin() >= i.begin() and pos.begin() <= i.end():
                        print("DUPLICATE ["+str(index)+"] ("+str(i.begin())+", "+str(i.end())+"): "+view.substr(i))




class OverkodeFileData:

    def __init__(self, name):
        self.name = name
        self.current_counter = 0
        self.document_size = 0
        self.last_document_size = 0
        self.total_rows = 0
        self.last_total_rows = 0

    def print_values(self):
        print("{\n\tname: "+str(self.name)+"\n\tcurrent_counter: "+str(self.current_counter)+"\n\tdocument_size: "+str(self.document_size)+"\n\tlast_document_size: "+str(self.last_document_size)+"\n\ttotal_rows: "+str(self.total_rows)+"\n\tlast_total_rows: "+str(self.last_total_rows)+"\n}")




class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """ Create a new project"""
        #TODO: Publicar el link en una vista nueva
        print("Runing a main\n")
        # test() 

        # core.main()



        
        # allcontent = sublime.Region(0, self.view.size())
        # selected_text = self.view.sel()
        # self.view.replace(edit, allcontent, 'Hello, world!')
        # self.view.insert(edit, self.view.sel()[0].begin(), '                               ,|     \n                             //|                              ,|\n                           //,/                             -~ |\n                         // / |                         _-~   /  ,\n                       /\'/ / /                       _-~   _/_-~ |\n                      ( ( / /\'                   _ -~     _-~ ,/\'\n                       \\~\\/\'/|             __--~~__--\\ _-~  _/,\n               ,,)))))));, \\/~-_     __--~~  --~~  __/~  _-~ /\n            __))))))))))))));,>/\\   /        __--~~  \\-~~ _-~\n           -\\(((((\'\'\'\'(((((((( >~\\/     --~~   __--~\' _-~ ~|\n  --==//////((\'\'  .     `)))))), /     ___---~~  ~~\\~~__--~ \n          ))| @    ;-.     (((((/           __--~~~\'~~/\n          ( `|    /  )      )))/      ~~~~~__\\__---~~__--~~--_\n             |   |   |       (/      ---~~~/__-----~~  ,;::\'  \\         ,\n             o_);   ;        /      ----~~/           \\,-~~~\\  |       /|\n                   ;        (      ---~~/         `:::|      |;|      < >\n                  |   _      `----~~~~\'      /      `:|       \\;\\_____// \n            ______/\\/~    |                 /        /         ~------~\n          /~;;.____/;;\'  /          ___----(   `;;;/               \n         / //  _;______;\'------~~~~~    |;;/\\    /          \n        //  | |                        /  |  \\;;,\\              \n       (<_  | ;                      /\',/-----\'  _>\n        \\_| ||_                     //~;~~~~~~~~~ \n            `\\_|                   (,~~ \n                                    \\~\\ \n                                     ~~ \n')
        # self.view.replace(edit,allcontent,'                               ,|     \n                             //|                              ,|\n                           //,/                             -~ |\n                         // / |                         _-~   /  ,\n                       /\'/ / /                       _-~   _/_-~ |\n                      ( ( / /\'                   _ -~     _-~ ,/\'\n                       \\~\\/\'/|             __--~~__--\\ _-~  _/,\n               ,,)))))));, \\/~-_     __--~~  --~~  __/~  _-~ /\n            __))))))))))))));,>/\\   /        __--~~  \\-~~ _-~\n           -\\(((((\'\'\'\'(((((((( >~\\/     --~~   __--~\' _-~ ~|\n  --==//////((\'\'  .     `)))))), /     ___---~~  ~~\\~~__--~ \n          ))| @    ;-.     (((((/           __--~~~\'~~/\n          ( `|    /  )      )))/      ~~~~~__\\__---~~__--~~--_\n             |   |   |       (/      ---~~~/__-----~~  ,;::\'  \\         ,\n             o_);   ;        /      ----~~/           \\,-~~~\\  |       /|\n                   ;        (      ---~~/         `:::|      |;|      < >\n                  |   _      `----~~~~\'      /      `:|       \\;\\_____// \n            ______/\\/~    |                 /        /         ~------~\n          /~;;.____/;;\'  /          ___----(   `;;;/               \n         / //  _;______;\'------~~~~~    |;;/\\    /          \n        //  | |                        /  |  \\;;,\\              \n       (<_  | ;                      /\',/-----\'  _>\n        \\_| ||_                     //~;~~~~~~~~~ \n            `\\_|                   (,~~ \n                                    \\~\\ \n                                     ~~ \n')
        # print(selected_text)
        # for view in selected_text:
        #   print(view)



class RowjumpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """ Create a new project"""
        self.view.insert(edit, self.view.sel()[0].begin(), '\\n')






# from xml.etree import ElementTree as ET
# import urllib

# GOOGLE_AC = r"http://google.com/complete/search?output=toolbar&q=%s"

# class GoogleAutocomplete(sublime_plugin.EventListener):
#     def on_query_completions(self, view, prefix, locations):
#         elements = ET.parse(
#             urllib.request.urlopen(GOOGLE_AC % prefix)
#         ).getroot().findall("./CompleteSuggestion/suggestion")

#         sugs = [(x.attrib["data"],) * 2 for x in elements]

#         return sugs


# import sublime
# import sublime_plugin, re, string   #import the required modules

# class ExampleCommand(sublime_plugin.TextCommand): #create Webify Text Command
#   def run(self, edit):   #implement run method
#       for region in self.view.sel():  #get user selection
#           if not region.empty():  #if selection not empty then
#               s = self.view.substr(region)  #assign s variable the selected region                
#               news = s.replace('<', '&lt;')
#               news = news.replace('>', '&gt;')
#               self.view.replace(edit, region, news) #replace content in view
