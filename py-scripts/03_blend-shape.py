'''
	OBJECTIVE
	Given a series of mesh with different shape/layout, excute blending of the last selected towards the others

	Usage Example:
	1) Create in the scene 3 meshes (diffent in shapes)
	2) Select all the meshes and at last the one to apply the blending
	3) Run the program and execute the blenind throught the UI
'''

from maya import cmds

BSM_TEXT_SCROLL_LIST = "bsmList"
BSM_FLOAT_SLIDER_GRP = "slider"

def blend_shape_manager_ui():
    win_name = "blend_shape_manager_ui"
    
    if cmds.window(win_name, q=True, ex=True):
        cmds.deleteUI(win_name)
    
    cmds.window(win_name, title="Blend Shape Manager")
    cmds.columnLayout()    
    cmds.textScrollList(BSM_TEXT_SCROLL_LIST, allowMultiSelection=True, doubleClickCommand=apply_blend_listener)
    cmds.floatSliderGrp(BSM_FLOAT_SLIDER_GRP, field=True, minValue=0, maxValue=1, dragCommand=slider_listener)
    cmds.button(label="Refresh", command=refresh_listener)
    cmds.button(label="Reset", command=reset_listener)
    cmds.setParent("..")
    
    cmds.showWindow(win_name)

def reset_listener(*args):
    bsn = get_blend_shape_node()
    attrs = cnds.listAttr(blend_shape_node+".weight", m=True)
    for attr in attrs:
        cmds.setAttr(bsn+"."+attr, 0)
    
def refresh_listener(*args):    
    bsn = get_blend_shape_node()
    if not bsn: 
        print("[WARN] Selected elements has no blend shapes")
        return
    cmds.textScrollList(BSM_TEXT_SCROLL_LIST, edit=True, removeAll=True)

    attrs = cnds.listAttr(blend_shape_node+".weight", m=True)
    for attr in attrs:
        cmds.textScrollList(BSM_TEXT_SCROLL_LIST, edit=True, append=attr)



def apply_blend_listener():
    reset_listener()
    bsn = get_blend_shape_node()
    scrollSelection = cmds.textScrollList(BSM_TEXT_SCROLL_LIST, query=True, selectItem=True)
    selected = scrollSelection[0]
    cmds.setAttr(bsn+"."+selected, 1)


def get_blend_shape_node():
    selection = cmds.ls(selection=True)
    history = cmds.listHistory(selection[0])
    blend_shape_node = ""

    for node in history:
        if cmds.nodeType(node) == "blendShape":
            blend_shape_node = node
            break
    return blend_shape_node

def slider_listener(*args):
    bsn = get_blend_shape_node()
    attrs = cmds.textScrollList(BSM_TEXT_SCROLL_LIST, query=True, selectItem=True)
    # list compression
    attrs_array = [bsn + "." + attr for attr in attrs]
    # con "*" spacchetto la lista mettendo "," tra gli elementi
    cmds.connectControl(BSM_FLOAT_SLIDER_GRP, *attrs_array) 

blend_shape_manager_ui()
    

