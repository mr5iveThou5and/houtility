#!/usr/bin/python


#import hou, os, sys, datetime

def msg(m):
    msg = "[%s OnCreated.py] %s" % (datetime.datetime.now().strftime("%y%m%d %H:%M.%S"), m)
    sys.__stderr__.write(msg+"\n")
    #print msg

def dbg(m):
    msg('(debug) %s' % m)


def colorize_op(kwargs):
    '''.'''
    gcs = {
        'cam':                              (0.5, 0.5, 0.5),

        'fetch':                            (0.7, 1.0, 0.7),

        #'geo':                             (0.6, 0.6, 0.6),

        'hlight':                           (1.0, 1.0, 0.4),
        'hlight::2.0':                      (1.0, 1.0, 0.4),
        'ambient':                          (1.0, 1.0, 0.4),
        'envlight':                         (1.0, 1.0, 0.4),
        'indirectlight':                    (1.0, 1.0, 0.4),

        'shopnet':                          (0.6, 0.4, 0.2),
        'material':                         (0.6, 0.4, 0.2),
        'vopmaterial':                      (0.6, 0.4, 0.2),
        'vopsurface':                       (0.6, 0.4, 0.2),
        'vopcvex':                          (0.0, 0.6, 1.0),
        
        'vm_geo_ptreplicate':               (0.4, 1.0, 0.4),
        'vm_geo_vexvolume':                 (0.4, 1.0, 0.4),
        'vm_geo_sprite':                    (0.4, 1.0, 0.4),
        'vm_geo_program':                   (0.4, 1.0, 0.4),
        'vm_geo_ptinstance':                (0.4, 1.0, 0.4),
        'vm_geo_fur':                       (0.4, 1.0, 0.4),
        'vm_geo_file':                      (0.4, 1.0, 0.4),
        'vm_geo_alembic':                   (0.4, 1.0, 0.4),

        'cache':                            (0.6, 0.6, 1.0),
        'object_merge':                     (0.7, 1.0, 0.7),

        'dopnet':                           (0.6, 0.6, 1.0),
        'dopio':                            (0.6, 0.6, 1.0),
        'dopimportfield':                   (0.6, 0.6, 1.0),
        'dopimportrecords':                 (0.6, 0.6, 1.0),
        'dopimport':                        (0.6, 0.6, 1.0),
        'solver':                           (0.6, 0.6, 1.0),

        'bulletrbdsolver':                  (0.6, 0.6, 1.0),
        'flipsolver::2.0':                  (0.6, 0.6, 1.0),
        'whitewatersolver':                 (0.6, 0.6, 1.0),
        'smokesolver::2.0':                 (0.6, 0.6, 1.0),
        'sopsolver':                        (0.6, 0.6, 1.0),
        'finiteelementsolver':              (0.6, 0.6, 1.0),
        'staticsolver':                     (0.6, 0.6, 1.0),
        'pyrosolver::2.0':                  (0.6, 0.6, 1.0),
        'popsolver::2.0':                   (0.6, 0.6, 1.0),
        'rbdsolver':                        (0.6, 0.6, 1.0),
        'rigidbodysolver':                  (0.6, 0.6, 1.0),
        'odesolver':                        (0.6, 0.6, 1.0),


        'ropnet':                           (0.2, 0.0, 0.4),
        'chopnet':                          (0.0, 0.4, 0.0),
        'cop2net':                          (0.4, 1.0, 1.0),
        'vopnet':                           (0.8, 0.6, 0.0),

        'global':                           (0.6, 0.6, 1.0),

        'ifd':                              (1.0, 1.0, 1.0),

        'output':                           (0, 0, 0),

        'lastone':                          (0,0,0)
    }
    # Context Sensitive
    cs = {
        'Sop/null':                         (0, 0, 0),
        'Sop/subnet':                       (0.996, 0.933, 0),
        'Sop/file':                         (0.867, 0, 0),
        'Sop/rop_geometry':                 (0.867, 0, 0),
        'Sop/filecache':                    (0.867, 0, 0),
        'Sop/filemerge':                    (0.867, 0, 0),
        'Sop/mdd':                          (0.867, 0, 0),
        'Sop/alembic':                      (0.867, 0, 0),
        'Sop/rop_alembic':                  (0.867, 0, 0),
        'Driver/dop':                       (0.6, 0.6, 1.0),
        'Driver/geometry':                  (0.867, 0, 0),
        'Driver/null':                      (0, 0, 0),
        'Driver/merge':                     (0, 0, 0),
        'Vop/bind':                         (0.6, 0.6, 1.0),

        'lastone':                          (0,0,0)
    }

    try:
        N = kwargs['node']
        n = kwargs['node'].name()
        t = kwargs['type'].nameWithCategory()
        gt = kwargs['type'].name()

        # Print debugging message
        #dbg('node=%s type=%s' % (n, t, ))

        # Intialize default grey color
        # This gets rid of the new auto coloring introduced in 16.0
        N.setColor( hou.Color( (0.8, 0.8, 0.8) ) )


        '''
            COLOR NODES
        '''
        # gt is global type like 'null' would apply to all contexts
        if gt in gcs:
            N.setColor( hou.Color( gcs[gt] ) )
        # t is context sensitive so it let's you know like 'Sop/file'
        if t in cs:
            N.setColor( hou.Color( cs[t] ) )


        '''
            NODE SPECIFIC PRESETS
        '''
        # Maybe some nodes we want to do something to them every time (change default settings)
        if gt == 'cam':
            N.parm('resx').set(1280)
            N.parm('resy').set(515)
            #N.parm('aperture').set(36)
        if gt == 'fetch':
            N.setDisplayFlag(False) 
        if gt == 'output':
            N.setName('OUT', unique_name=True)
        if t == 'Sop/file':
            N.parm('missingframe').set('empty')
        if t == 'Sop/null':
            parm_group = N.parmTemplateGroup()             
            folder_scripts = hou.FolderParmTemplate("folder0", "scripts", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)

            hou_parm_template = hou.ButtonParmTemplate("make_bbox", "make_bbox")
            hou_parm_template.hideLabel(True)   # This will align the button to the leftmost side of the UI and eliminate the gap
            hou_parm_template.setScriptCallback("import kunz_utils; reload(kunz_utils);  kunz_utils.make_bbox(hou.pwd(), 0)")
            hou_parm_template.setScriptCallbackLanguage(hou.scriptLanguage.Python)
            hou_parm_template.setTags({"script_callback": "import kunz_utils; reload(kunz_utils);  kunz_utils.make_bbox(hou.pwd(), 0)", "script_callback_language": "python"})
            folder_scripts.addParmTemplate(hou_parm_template)

            hou_parm_template = hou.ButtonParmTemplate("make_object_merge", "make_object_merge")
            hou_parm_template.hideLabel(True)   # This will align the button to the leftmost side of the UI and eliminate the gap
            hou_parm_template.setScriptCallback("import kunz_utils; reload(kunz_utils);  kunz_utils.make_obj_merge(hou.pwd())")
            hou_parm_template.setScriptCallbackLanguage(hou.scriptLanguage.Python)
            hou_parm_template.setTags({"script_callback": "import kunz_utils; reload(kunz_utils);  kunz_utils.make_bbox(hou.pwd(), 0)", "script_callback_language": "python"})
            folder_scripts.addParmTemplate(hou_parm_template)

            parm_group.append(folder_scripts)
            

            folder_geo_info = hou.FolderParmTemplate("folder0", "geo_info", folder_type=hou.folderType.Tabs, default_value=0, ends_tab_group=False)
            
            # http://forums.odforce.net/topic/15487-setting-an-expression-as-default-value-solved/
            hou_parm_template = hou.FloatParmTemplate("centroid", "centroid", 3, default_expression=("centroid(opinputpath('.',0),0)", "centroid(opinputpath('.',0),1)", "centroid(opinputpath('.',0),2)"), default_expression_language=(hou.scriptLanguage.Hscript, hou.scriptLanguage.Hscript, hou.scriptLanguage.Hscript))
            folder_geo_info.addParmTemplate(hou_parm_template)
            
            hou_parm_template = hou.FloatParmTemplate("bbox_size", "bbox_size", 3, default_expression=("bbox(opinputpath('.',0),D_XSIZE)", "bbox(opinputpath('.',0),D_YSIZE)", "bbox(opinputpath('.',0),D_ZSIZE)"), default_expression_language=(hou.scriptLanguage.Hscript, hou.scriptLanguage.Hscript, hou.scriptLanguage.Hscript))
            folder_geo_info.addParmTemplate(hou_parm_template)
            '''
            hou_parm_template = hou.IntParmTemplate("npoints", "npoints", 1, default_expression=("npoints(opinputpath('.',0))"), default_expression_language=(hou.scriptLanguage.Hscript))
            folder_geo_info.addParmTemplate(hou_parm_template)
            '''
            hou_parm_template = hou.IntParmTemplate("npoints", "npoints", 1, default_value=([0]), min=0, max=1048576, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1)
            folder_geo_info.addParmTemplate(hou_parm_template)
            hou_parm_template = hou.IntParmTemplate("nprims", "nprims", 1, default_value=([0]), min=0, max=8192, min_is_strict=False, max_is_strict=False, naming_scheme=hou.parmNamingScheme.Base1)
            folder_geo_info.addParmTemplate(hou_parm_template)           
            parm_group.append(folder_geo_info)

            # Set expressions in the paramters we just created
            N.setParmTemplateGroup(parm_group)
            for i in range(3):
                expr_keyframe = hou.Keyframe()
                expr_keyframe.setTime(0)
                expr_keyframe.setExpression("centroid(opinputpath(\'.\',0)," + str(i) + ")", hou.exprLanguage.Hscript)
                N.parmTuple('centroid')[i].setKeyframe(expr_keyframe)
            for i in range(3):
                component = ''
                if i == 1:
                    component = 'D_YSIZE'
                elif i == 2:
                    component = 'D_ZSIZE'
                else:
                    component = 'D_XSIZE'
                expr_keyframe = hou.Keyframe()
                expr_keyframe.setTime(0)
                expr_keyframe.setExpression("bbox(opinputpath(\'.\',0)," + component + ")", hou.exprLanguage.Hscript)
                N.parmTuple('bbox_size')[i].setKeyframe(expr_keyframe)

            # npoints() expr
            expr_keyframe = hou.Keyframe()
            expr_keyframe.setTime(0)
            expr_keyframe.setExpression("npoints(opinputpath(\'.\',0))", hou.exprLanguage.Hscript)
            N.parm('npoints').setKeyframe(expr_keyframe)

            # nprims() expr
            expr_keyframe = hou.Keyframe()
            expr_keyframe.setTime(0)
            expr_keyframe.setExpression("nprims(opinputpath(\'.\',0))", hou.exprLanguage.Hscript)
            N.parm('nprims').setKeyframe(expr_keyframe)
        if t == 'Sop/xform':
            N.setName('xform1', unique_name=True)
            '''
            for i in range(3):
                expr_keyframe = hou.Keyframe()
                expr_keyframe.setTime(0)
                expr_keyframe.setExpression("centroid(opinputpath(\'.\',0)," + str(i) + ")", hou.exprLanguage.Hscript)
                N.parmTuple("p")[i].setKeyframe(expr_keyframe)
            '''
        if t == 'Sop/box':
            N.parm('vertexnormals').set(True)
        if gt == 'dopnet':
            N.parm('interpolate').set(False)
            parm_group = N.parmTemplateGroup() 
            N.setParmTemplateGroup(parm_group)
            hou_parm_template = hou.ButtonParmTemplate("toggle_opencl", "Toggle OpenCL")
            hou_parm_template.setScriptCallback("import kunz_utils; reload(kunz_utils);  kunz_utils.toggle_opencl(hou.pwd())")
            hou_parm_template.setScriptCallbackLanguage(hou.scriptLanguage.Python)
            hou_parm_template.setTags({"script_callback": "import kunz_utils; reload(kunz_utils);  kunz_utils.toggle_opencl(hou.pwd())", "script_callback_language": "python"})
            parm_group.append(hou_parm_template)
            N.setParmTemplateGroup(parm_group)



    except:
        pass

colorize_op(kwargs)





# Auto save the scene on node creation
# Only saves a backup every 10 mins
# Do this by checking if a save file exists from the last 10 min
import kunz_auto_save
reload(kunz_auto_save)
kunz_auto_save.kunz_auto_save()
