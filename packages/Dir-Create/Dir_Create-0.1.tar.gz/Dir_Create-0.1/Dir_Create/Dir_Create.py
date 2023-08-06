#import os, shutil, subprocess

class Create_Directory:

    # Initialize class object
    def __init__(self, dir):
        ''' dir = the directory where to create the Project folder. '''
        self.directory = dir

        # Delete pre-existing directories named "Project"
        os.chdir(self.directory)
        if os.path.exists('./Project'):
            shutil.rmtree('./Project')
 
    # Initialize tasks
    def create_dir(self, n, draft, slides):
        ''' n = number of tasks to inizialise'''

        # Initialize tasks' structure
        for i in range(n):
            self.task_i = './Project/tasks/task' + str(i+1) + '/input/'
            self.task_c = './Project/tasks/task' + str(i+1) + '/code/'
            self.task_o = './Project/tasks/task' + str(i+1) + '/output/'
            os.makedirs(self.task_i), os.makedirs(self.task_c), os.makedirs(self.task_o)

        # Initialize Main.py file for each task
        for i in range(n):
            with open('./Project/tasks/task' + str(i+1) + '/code/' + 'Main.py', "w") as file:
                #file.write("#!/usr/bin/env python") # Make it executable
                file.write("#!/usr/bin/env python\nprint(" + str(i+1) + ")") # Make Main.py executable

        # Initialize slides and or draft
        if slides == True:
            os.makedirs('./Project/slides/')
        if draft == True:
            os.makedirs('./Project/draft/')

        # Initialize file to execute all Main.py from tasks
        os.makedirs('./Project/execute/')
        with open('./Project/execute/execute_all.py', "w") as file:
            file.write("import os")
            file.write("\n ")
            file.write("\n#Execute Main files of each task")
            for i in range(n):
                string0 = "#Call task" + str(i+1)
                string1 = "os.system('chmod +x " + self.directory + "/Project/tasks/task" + str(i+1) + "/code/Main.py')"
                string2 = "os.system('" + self.directory + "/Project/tasks/task" + str(i+1) + "/code/Main.py')"
                file.write("\n" + "\n"+ string0 + "\n" + string1 + "\n" + string2)

d = Create_Directory('/Users/Faber/Desktop')
d.create_dir(3,True,True)