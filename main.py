import os
from tinydb import TinyDB, Query
import PySimpleGUI.PySimpleGUI as sg
import logging

logging.basicConfig(filename="main.log",
                    level=logging.DEBUG,
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    filemode = "w")

class Main:
    def __init__(self):

        self.database_path = os.getcwd() + "/database"
        self.tasks_path = self.database_path + "/tasks.json"

        if os.path.exists(self.database_path):
            self.tasks = TinyDB(self.tasks_path) 

    def setup(self):
        try:
            os.mkdir("database")
            os.chdir(self.database_path)
            TinyDB(self.tasks_path)
        except FileExistsError:
            pass
        except OSError:
            logging.warning("Unable to create necessary files")

    def add_task(self, task_to_add):
        task_to_add = str(task_to_add)
        self.tasks.insert({
            "task": task_to_add,
            "completed" : False # Returns 0
        })

    def mark_completed(self, completed_task):
        self.tasks.upsert({
            "task": completed_task,
            "completed": True # Returns 1
            }, Query().task == str(completed_task) ) # Search via key, then update completed condition 

    def mark_uncompleted(self, uncompleted_task):
        self.tasks.upsert({
            "task": uncompleted_task,
            "completed": False
            }, Query().task == str(uncompleted_task) ) 

    remove_task = lambda self, task_to_remove: self.tasks.remove(Query().task.search(str(task_to_remove)))

    task_list = lambda self: self.tasks.all()

    reset_tasks = lambda self: self.tasks.purge()
    
    def formatted_tasklist(self):
        formatted_tasklist = [] 
        for task in self.tasks.all():
            if task["completed"] == 0: 
                formatted_tasklist.append(task["task"])
        return formatted_tasklist
    
    def formatted_completedlist(self):
        formatted_completedlist = []
        for task in self.tasks.all():
            if task["completed"] == 1:
               formatted_completedlist.append(task["task"])
        return formatted_completedlist

if __name__ == "__main__":

    main = Main()
    if not os.path.exists(main.tasks_path): 
        main.setup()
        
    def layout(): # Main layout
   
        sg.theme('LightGrey1')
        layout = [
                    [sg.Button('Add Task', button_color = ('black', 'lightgrey')), sg.InputText(key="TASK", enable_events = True, size=(65,1))],
                    [sg.Button('Close', button_color = ('white', 'grey')), sg.Button('Reset Task List', button_color = ('black', 'lightgrey'))],
                    [sg.Listbox(main.formatted_tasklist(), size=(35,10), enable_events = True, key="LIST"), sg.Listbox(main.formatted_completedlist(), size=(35,10), enable_events = True, key="COMPLETEDLIST")],
                 ]

        window = sg.Window('Task Manager', layout, font=("Monaco",10) )
        return window

    window = layout()
   
    # Event functions
    def on_task_click(*args):
        value = window["LIST"].get()
        for i in value:
            if not i.isspace():
                main.mark_completed(i)
                logging.debug("Moved {} to COMPLETEDLIST".format(i))

    def on_completedtask_click(*args):
        value = window["COMPLETEDLIST"].get()
        for i in value:
            main.mark_uncompleted(i)
            logging.debug("Moved {} to LIST".format(i))
            
    # TODO: Add remove function

    while True: # Event Loop
        event, values = window.read()
        main.formatted_tasklist()
        
        # Binded events
        window["LIST"].bind("<Button-1>", on_task_click())
        window["COMPLETEDLIST"].bind("<Button-1>", on_completedtask_click()) 

        if event in ('Add Task'): #Add user task to listbox
            main.add_task(values["TASK"])
            window["TASK"].update("") # Remove entry from input
            logging.debug("{}: {}".format(event,values["TASK"]))

        if event in ("Add Completed"):
            main.mark_completed(values["TASK"])
            window["TASK"].update("") # Remove entry from input
            logging.debug("{}: {}".format(event,values["TASK"]))

        if event in ('Reset Task List'):
            main.reset_tasks()
            logging.debug(event)
        
	# Keeps listboxs up-to-date 
        window["LIST"].update(main.formatted_tasklist())
        window["COMPLETEDLIST"].update(main.formatted_completedlist())
 
        if event in ('Close'):
            break
            logging.debug(event)
        
    window.close()
    
