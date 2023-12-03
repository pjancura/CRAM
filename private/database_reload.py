'''
the purpose of this script is to reset the database 
'''

import os
import shutil

# delete the old  storage.sqlite file
try:
    os.remove("/home/pert2/web2py/applications/CRAM/databases/storage.sqlite")
except:
    print(FileNotFoundError, "unable to delete old storage.sqlite")
else:
# put a clean copy of the database into the databases folder
    try:
        shutil.copy2("/home/pert2/web2py/applications/CRAM/private/storage.sqlite", "/home/pert2/web2py/applications/CRAM/databases")
    except:
        print("unable to copy / paste")
    else:
        print("success!")
