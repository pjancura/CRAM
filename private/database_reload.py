'''
the purpose of this script is to reset the database 
'''

import os
import shutil

# delete the old  storage.sqlite file
try:
    os.remove("CRAM/databases/storage.sqlite")
except:
    print(FileNotFoundError)
else:
# put a clean copy of the database into the databases folder
    try:
        shutil.copy2("storage.sqlite", "CRAM/databases")
    except:
        print("unable to copy / paste")
    else:
        print("success!")
