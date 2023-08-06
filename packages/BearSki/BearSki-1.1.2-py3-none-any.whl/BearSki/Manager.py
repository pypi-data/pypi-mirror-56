import os
import shutil
import sys
from BearSki.testproject_template import BasicTestProject


def copy_file(source,target):

  if not os.path.exists(target):
    # create the folders if not already exists
    os.makedirs(target)
  try:
    shutil.copy(source, target)
  except IOError as e:
    print("Unable to copy file. %s" % e)
  except:
    print("Unexpected error:", sys.exc_info())
  

def creat_test_project(projectname):

    BasicTestProject.create_testproject(projectname)

    



