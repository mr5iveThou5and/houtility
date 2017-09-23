import hou

'''
    TO-DO

    make_RNDR
    Create a render object fetching the current node
'''

def make_obj_merge(node):
    om = node.parent().createNode('object_merge', 'get__'+node.name(), run_init_scripts=True, load_contents=True, exact_type_name=True)
        
    om.setPosition(node.position())
    #om.moveToGoodPosition()
    om.move(hou.Vector2(1, -1))
    om.parm('objpath1').set(om.relativePathTo(node))
    om.parm('xformtype').set('none')

def make_bbox(node, enable_expr_links):
    '''
    Create a box sop with dimensions mathcing the bounding box of the input node
    enable_expr_links will toggle between hardcoded values or relative references of the bounding box dimensions
    '''
    bb = node.parent().createNode('box', 'bbox1', run_init_scripts=True, load_contents=True, exact_type_name=True)
    bb.setPosition(node.position())
    #bb.moveToGoodPosition()
    bb.move(hou.Vector2(1, -1))

    if enable_expr_links == 0:
        bbox_scale = node.geometry().boundingBox().sizevec()
        bbox_center = node.geometry().boundingBox().center()
        for i in range(3):
            bb.parmTuple('size')[i].set(bbox_scale[i])
        for i in range(3):
            bb.parmTuple('t')[i].set(bbox_center[i])
    
    if enable_expr_links == 1:
        for i in range(3):
            expr_keyframe = hou.Keyframe()
            expr_keyframe.setTime(0)
            component = ''
            if i == 1:
                component = 'D_YSIZE'
            elif i == 2:
                component = 'D_ZSIZE'
            else:
                component = 'D_XSIZE'
            expr_keyframe.setExpression("bbox('" + bb.relativePathTo(node) + "'," + component + ")", hou.exprLanguage.Hscript)
            bb.parmTuple('size')[i].setKeyframe(expr_keyframe)
        for i in range(3):
            expr_keyframe = hou.Keyframe()
            expr_keyframe.setTime(0)
            expr_keyframe.setExpression("centroid('" + bb.relativePathTo(node) + "'," + str(i) + ")", hou.exprLanguage.Hscript)
            bb.parmTuple('t')[i].setKeyframe(expr_keyframe)
    
    bb.parm('vertexnormals').set(True)

def toggle_opencl(parent_node):
    for node in parent_node.allSubChildren():
        for p in node.parms():
            if p.name()=='opencl':
                try:
                    p.set(1-p.eval())
                except hou.PermissionError: #this handles the case that the parm is inside of a locked .otl
                    pass
