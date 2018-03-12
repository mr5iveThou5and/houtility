import time
import hou

# Save a backup of the current Houdini session
def saveArchive():
    # Get the file path of the current Houdini session
    # (Equivalent to $HIP/$HIPNAME)
    ogFile = hou.hipFile.path()
    # What do we want to save the archive file as?
    fileStr =  hou.getenv("HIP")+"/backup/BKUP_"+time.strftime("%Y%m%d%H%M%S")+"_"+hou.hipFile.basename()
    # Make sure this is a string (I was getting errors if I didn't do this)
    fileStr = str(fileStr)
    # Save the archive file
    hou.hipFile.save(file_name=fileStr, save_to_recent_files=False)
    # Revert the name of the Houdini session to what it was prior to executing this function
    hou.hipFile.setName(ogFile)
    # Return the path of the newly saved file
    return fileStr
