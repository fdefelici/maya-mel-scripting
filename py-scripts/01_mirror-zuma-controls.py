''' OBJECTIVE
    Given a mesh with animation controls the program offer those two features:
    - Mirroring selected controls making the other side symmetrical. 
	- Switching selected controls inverting the two sides.
'''


import maya.cmds as cmds

# COMMAND SAMPLES:
#  cmds.ls(['*_ac_*','*_fk_*'], type='nurbsCurve' )
#  cmds.listAttr("zoma_ac_lf_footik", keyable=True, userDefined=True)
#  cmds.ls(['*_ac_lf_*'], type='nurbsCurve' )        
#  cmds.listRelatives("zoma_ac_lf_footik", parent=True)[0]

#############################################################
#########  FEATURE: MIRRORING ###############################
#############################################################
def copy_attribs(from_obj, to_obj):
    #attributi base
    defaultAttrs =  cmds.listAttr(from_obj, keyable=True)
    for eachAttr in defaultAttrs:
        if (eachAttr.startswith("translate") or
            eachAttr.startswith("rotate") or
            eachAttr.startswith("scale") ):
            val = cmds.getAttr(from_obj+"."+eachAttr)
            cmds.setAttr(to_obj+"."+eachAttr, val)
    #attributi user defined
    userAttrs = cmds.listAttr(from_obj, keyable=True, userDefined=True)
    if userAttrs == None: return
    for eachAttr in userAttrs:
        val = cmds.getAttr(from_obj+"."+eachAttr)
        cmds.setAttr(to_obj+"."+eachAttr, val)


LEFT_TO_RIGHT = "lf2rt"
RIGHT_TO_LEFT = "rt2lf"
def mirror_controls(mode):
    sourceFilter = []
    destinFilter = []
    if (mode == LEFT_TO_RIGHT):
        sourceFilter = ['*_ac_lf_*','*_fk_lf_*']
        destinFilter = ['*_ac_rt_*','*_fk_rt_*']
    elif (mode == RIGHT_TO_LEFT):    
        sourceFilter = ['*_ac_rt_*','*_fk_rt_*']
        destinFilter = ['*_ac_lf_*','*_fk_lf_*']
    else:
        cmds.error("Wrong mode: %s" + mode)
    
    sources = cmds.ls(sourceFilter, type='nurbsCurve' )
    destins = cmds.ls(destinFilter, type='nurbsCurve' )
    
    for i in range(len(sources)):
       eachSource = cmds.listRelatives(sources[i], parent=True)[0]
       eachDestin = cmds.listRelatives(destins[i], parent=True)[0]
       copy_attribs(eachSource, eachDestin)


#############################################################
#########  FEATURE: SWITCHING ###############################
#############################################################
def switch_attribs(from_obj, to_obj):
    #attributi base
    defaultAttrs =  cmds.listAttr(from_obj, keyable=True)
    for eachAttr in defaultAttrs:
        if (eachAttr.startswith("translate") or
            eachAttr.startswith("rotate") or
            eachAttr.startswith("scale") ):
            val_from = cmds.getAttr(from_obj+"."+eachAttr)
            val_to   = cmds.getAttr(to_obj+"."+eachAttr)
            cmds.setAttr(from_obj+"."+eachAttr, val_to)
            cmds.setAttr(to_obj+"."+eachAttr, val_from)
    #attributi user defined
    userAttrs = cmds.listAttr(from_obj, keyable=True, userDefined=True)
    if userAttrs == None: return
    for eachAttr in userAttrs:
        val_from = cmds.getAttr(from_obj+"."+eachAttr)
        val_to   = cmds.getAttr(to_obj+"."+eachAttr)
        cmds.setAttr(from_obj+"."+eachAttr, val_to)
        cmds.setAttr(to_obj+"."+eachAttr, val_from)

def switch_controls():    
    lf_ctrls = cmds.ls(['*_ac_lf_*','*_fk_lf_*'], type='nurbsCurve' )
    rt_ctrls = cmds.ls(['*_ac_rt_*','*_fk_rt_*'], type='nurbsCurve' )
    
    for i in range(len(lf_ctrls)):
       each_lf = cmds.listRelatives(lf_ctrls[i], parent=True)[0]
       each_rt = cmds.listRelatives(rt_ctrls[i], parent=True)[0]
       switch_attribs(each_lf, each_rt)



#############################################################
#########  TESTING    #######################################
#############################################################
def clean(): 
    cmds.select(all=True)
    cmds.delete()

def scenario01():
    cmds.file('C:\\_fdf\\projects\\workspace_aiv\\lessons\\LEZ47_20180424_MAYA_3_MEL\\model__zoma_hi_base_vanilla_rig_v6.ma',open=True, newFile=False, force=True)    
    cmds.setAttr("zoma_ac_lf_footik.rotateY", 45)


scenario01()

switch_controls()

mirror_controls(LEFT_TO_RIGHT)

clean()

