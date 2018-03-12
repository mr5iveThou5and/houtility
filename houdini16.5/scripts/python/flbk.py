import hou
import toolutils
import os
import subprocess
import string

# It's possible setting a $JOB path in the shell would cause this script to malfunction... The jpegs wouldn't get converted to movied and cleaned up
# Maybe setting $JOB messes up os.system() calls?

# CAN EXCECUTE WITH:
# import imp
# imp.load_source('', '../flbk.v1.py')

# some functions to assist in the automation of generating flipbooks from Houdini
# Latest updates: 2017 07 21
# Latest updates: 2018 02 10

def saveArchive(backup_directory):
    # Save a backup of the current Houdini session
    import time
    import hou

    # Get the file path of the current Houdini session
    # (Equivalent to $HIP/$HIPNAME)
    original_file = hou.hipFile.path()
    # Where to put the archive file?
    archive_dir = backup_directory
    # What do we want to save the archive file as?
    archive_file = time.strftime("%Y.%m.%d_%H.%M.%S")+'__'+hou.hipFile.basename()
    # Make sure this is a string (I was getting errors if I didn't do this)
    archive_file = str(archive_file)
    archive_file = archive_dir + '/' + archive_file

    if not os.path.exists(os.path.dirname(archive_file)):
        print 'Creating directory: '+os.path.dirname(archive_file)
        os.makedirs(os.path.dirname(archive_file))

    # Save the archive file
    hou.hipFile.save(file_name=archive_file, save_to_recent_files=False)
    # Revert the name of the Houdini session to what it was prior to executing this function
    hou.hipFile.setName(original_file)
    # Return the name of the session to what it was originally
    return archive_file

def which(program):
    import os
    # https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def main():
	# Get the path to the curreent scene file
    hip_file_path = hou.hipFile.path()
    # Parent dir of folder containing the hip_file_path
    houdini_dir = os.path.abspath(os.path.join(os.path.dirname(hou.hipFile.path()), os.pardir))

    # https://stackoverflow.com/questions/16513573/python-if-var-false
    if not os.path.exists(houdini_dir+'/flip'):
        print 'Creating directory: '+houdini_dir+'/flip'
        os.makedirs(houdini_dir+'/flip')

    # Put flipbooks in 'flip' folder
    flipbook_output_path = houdini_dir+'/flip/'+hou.getenv('HIPNAME')+'/$F4.JPEG'
    #flipbook_output_path = houdini_dir+'/flip/'+hou.getenv('HIPNAME')+'/$N.JPEG'

    # Save a backup of the scene file to the 'flip' folder as well
    backup_file_path = saveArchive(houdini_dir+'/flip/'+hou.getenv('HIPNAME'))
    # Output .mov path
    mp4_output_path = houdini_dir+'/flip/'+hou.getenv('HIPNAME')+'/'+os.path.splitext(os.path.split(backup_file_path)[1])[0]+'.mp4'

    # put quotes around this path to handle dir paths with spaces
    mp4_output_path = '"'+mp4_output_path+'"'

    if not os.path.exists(os.path.dirname(flipbook_output_path)):
            print 'Creating directory: '+os.path.dirname(flipbook_output_path)
            os.makedirs(os.path.dirname(flipbook_output_path))

    # Don't modifiy the existing settings (make a copy)
    flbk_settings = toolutils.sceneViewer().flipbookSettings().stash()

    # Set the output path
    print 'Flipbook output path: '+flipbook_output_path
    flbk_settings.output(flipbook_output_path)

    flbk_settings.outputToMPlay(0)

    '''
    # This won't preserve aspect ratio !!
    flbk_settings.useResolution(1)
    flbk_settings.resolution((512, 128))
    '''

    start = flbk_settings.frameRange()[0]
    end = flbk_settings.frameRange()[1]
    inc = flbk_settings.frameIncrement()

    '''
    hou.getenv('HIPNAME')
    hou.hipFile.path()
    hou.getenv('USER')
    hou.applicationVersionString()
    hou.applicationPlatformInfo()
    '''

    # Launch the flipbook
    toolutils.sceneViewer().flipbook(viewport=None, settings=flbk_settings, open_dialog=False)

    # Make me .JPEGs
    # We want to use a mild compression, by default Houdini saves them at full/loseless quality so their filesize is huge

    # Convert the output path to ffmpeg friendly %04d instead of Houdini's $F4 frame syntax
    flipbook_output_path = string.replace(flipbook_output_path, '$F4', '%04d')
    flipbook_output_path = '"'+flipbook_output_path +'"'

    # Make me a .mov
    # https://stackoverflow.com/questions/14430593/encoding-a-readable-movie-by-quicktime-using-ffmpeg
    # ffmpeg -i /tmp/%04d.JPEG -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -f mp4 -vcodec libx264 -pix_fmt yuv420p .v1.mp4
    # add -y to the command line after input file path to force overwriting if file exists
    # See link below for more info about adding metadata with ffmpeg
    # https://ubuntuforums.org/showthread.php?t=1193808
    # You can simply press enter where you want the newline as you are typing your command.
    # http://ffmpeg.gusari.org/viewtopic.php?f=11&t=3032
    # by default ffmpeg outputs 25fps, change this with: -r 24
    convert2mov_command = 'ffmpeg'
    convert2mov_command+=' -i '+string.replace(flipbook_output_path, '$F4', '%04d')
    convert2mov_command+=' -y'
    convert2mov_command+=' -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"'
    convert2mov_command+=' -f mp4 -vcodec libx264 -pix_fmt yuv420p'
    convert2mov_command+=' -r 24'
    # Set the Constant Rate Factor of the video
    # http://slhck.info/video/2017/02/24/crf-guide.html
    convert2mov_command+=' -crf 22'
    # Set the bitrate of the vide0
    # https://gist.github.com/ksharsha/b06d184391290bc3b87fdadadb73c5bc#file-ffmpeg-compress
    #convert2mov_command+=' -b:v 750k'
    convert2mov_command+=' -metadata title="'+hou.getenv('HIPNAME')+'"'
    # Metadata comment block:
    convert2mov_command+=' -metadata comment="'
    convert2mov_command+='SOURCE: '+hou.hipFile.path()+'\n'
    convert2mov_command+='SNAPSHOT: '+backup_file_path+'\n'
    convert2mov_command+='USER: '+hou.getenv('USER')+'\n'
    convert2mov_command+='VERSION: '+hou.applicationVersionString()+'\n'
    convert2mov_command+='PLATFORM: '+hou.applicationPlatformInfo()
    convert2mov_command+='"'
    # Metadata can be viewed using ffprobe, which comes with ffmpeg

    convert2mov_command+=' '+mp4_output_path

    print 'running "%s"' % convert2mov_command
    os.system(convert2mov_command)
    # Newline
    #os.system('echo')
    print 'done'

    # Taking temporary L on gif feature to finish main part
    # Make me a .gif
    #convert2gif_command = '/usr/local/bin/convert -loop 0 ' + src_frames + ' -fuzz 0% -layers Optimize ' + out_gif





    # Cleanup
    # Remove the .JPEGs generated by the flipbook

    # Remove the quotes at the beginning and ending of the path
    flipbook_output_path = flipbook_output_path.strip('"\'')
    # Replace the %04d ffmpeg frame indicator with * wildcard
    flipbook_output_path = flipbook_output_path.translate(None, "'").replace('%04d', '*')
    # This is done to handle paths that contain spaces, we have to encapsulate the dir path in quotes.
    # the wildcard part of the command must be outside the quotes, so that's why there's some dirname, basename finessing
    flipbook_output_path = '"'+os.path.dirname(flipbook_output_path)+'"' + '/' + os.path.basename(flipbook_output_path)
    
    command = 'rm -Rf %s' % flipbook_output_path
    #command+= str(flipbook_output_path)
    print 'running %s' % command
    os.system(command)

