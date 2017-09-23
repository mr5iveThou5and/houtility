import hou
import time
import os
import math

def kunz_auto_save():
  ogFile = hou.hipFile.path()
  sfile =  hou.getenv('HIP')+'/backup/AUTO_'+str(int(math.floor(float(time.strftime("%Y%m%d%H%M%S"))/1000.0))*1000)+'_'+os.path.splitext( hou.hipFile.basename() )[0]+'.'+str(os.getpid())+os.path.splitext( hou.hipFile.basename() )[1]
  sfile = str(sfile)
  if os.path.isfile(sfile) is False:
    hou.hipFile.save(file_name=sfile, save_to_recent_files=False)
    hou.hipFile.setName(ogFile) 
  else:
    sfile = ''

  return sfile
