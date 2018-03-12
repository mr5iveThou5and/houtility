import hou
import time
import os
import math

def kunz_auto_save():
    
    # This is the path of the current (live) scene file
    ogFile = hou.hipFile.path()

    # This is the path of the backup (archived) scene file
    # Gonna save it in a path relative to the current scene file, so get the $HIP env
    sfile =  hou.getenv('HIP')
    # Throw it in the backup folder in the $HIP dir
    sfile += '/backup/'

    # The rest of these string appends are simply assembling a super long file name, the directory has been chosen
    sfile += 'AUTO_'
    #sfile += str(int(math.floor(float(time.strftime("%Y%m%d%H%M%S"))/1000.0))*1000)
    # Better formatting (more readable date/time)
    sfile += time.strftime('%Y.%m.%d_%H') + '.' + str(int(math.floor(float(time.strftime('%M'))/10.0))*10)
    sfile += '_'
    # os.path.splitext( hou.hipFile.basename() ) returns something like (filename, extension), so [0] is the filename and [1] is the extension (hopefully .hip)
    sfile += os.path.splitext( hou.hipFile.basename() )[0]
    sfile += '.'
    sfile += str(os.getpid())
    # final step, add the file extension
    sfile += os.path.splitext( hou.hipFile.basename() )[1]
    # make sure the path is a string
    sfile = str(sfile)

    # make sure we aren't overwriting an existing backup file!
    if os.path.isfile(sfile) is False:
        hou.hipFile.save(file_name=sfile, save_to_recent_files=False)
        hou.hipFile.setName(ogFile) 
    else:
        sfile = ''

    # return the path of the backup we saved, if it's an empty string something went wrong!
    return sfile
