'''
the purpose of this script is to reset the database on my local build
'''

import os
import shutil

# delete the old  storage.sqlite file
try:
    os.remove("../databases/storage.sqlite")
except:
    print(FileNotFoundError, "unable to delete old storage.sqlite")
else:
# put a clean copy of the database into the databases folder
    try:
        shutil.copy2("storage.sqlite", "../databases")
    except:
        print("unable to copy / paste")
    else:
        print("success!")
