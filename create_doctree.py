from __future__ import print_function
from docfly import Docfly
import shutil
 
try:
    shutil.rmtree(r"source\ctmatching")
except Exception as e:
    print(e)
     
docfly = Docfly("ctmatching", dst="source")
docfly.fly()
