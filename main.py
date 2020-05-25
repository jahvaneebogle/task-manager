import os
from tinydb import TinyDB, Query
import PySimpleGUI.PySimpleGUI as sg

class Main:
    def __init__(self):
        self.database_path = os.getcwd() + "/database"
        self.tasks_path = self.database_path + "/tasks.json"
        self.completed_path = self.database_path + "/completed.json"

        if os.path.exists(self.database_path):
            self.tasks = TinyDB(self.tasks_path) 
            self.completed = TinyDB(self.completed_path)

    def setup(self):
        try:
            os.mkdir("database")
            os.chdir(self.database_path)
            TinyDB(self.tasks_path)
            TinyDB(self.completed_path)
        except FileExistsError:
            pass
        except OSError:
            print("Unable to create necessary files")

    def add_task(self, task_to_add):
        task_to_add = str(task_to_add)
        self.tasks.insert({
            "task": task_to_add
        })

    def add_completed_task(self, completed_task):
        self.tasks.remove(Query().task.search(str(completed_task))) 
        self.completed.insert({
            "completed task": completed_task
        })

    remove_task = lambda self, task_to_remove: self.tasks.remove(Query().task.search(str(task_to_remove)))
    remove_completed_task = lambda self, completed_to_remove: self.completed.remove(Query().completed.search(str(completed_to_remove)))

    task_list = lambda self: self.tasks.all()
    completed_list = lambda self: self.completed.all()

    reset_tasks = lambda self: self.tasks.purge()
    reset_completed_tasks = lambda self: self.completed.purge() 

if __name__ == "__main__":

    main = Main()
    if not os.path.exists(main.tasks_path and main.completed_path): 
        main.setup()

    def Layout(): # Main layout
        sg.theme('LightGreen')
        layout = [
                    [sg.Text('Add Task: '), sg.InputText(key="TASK")],
                    [sg.Button('Add Task'), sg.Button('Add Completed'), sg.Button('Reset Task List'), sg.Button('Close')],
                    [sg.Listbox(main.task_list(), size=(65,10),enable_events=True, key="LIST")]
                 ]

        window = sg.Window('Task Manager', layout, font="Monaco")
        return window

    window = Layout()

    while True: # Event Loop
        event, values = window.read()

        if event in ('Add Task'): #Add user task to listbox
            main.add_task(values["TASK"])
            window["TASK"].update("") # Remove commited entry from input
            print(main.task_list())
        
        if event in ('Reset Task List'):
            main.reset_tasks()
            print(main.task_list())
	
	# TODO: Add event on selection of task value
        ''' 
        if event in ("LIST"):
            main.remove_task(values[event])
            print(main.task_list())
       ''' 
        if event in ('Close'):
            break
       	
	# Keep task list up-to-date 
        window["LIST"].update(main.task_list())

        print('You entered ', values["TASK"])

    window.close()
    
