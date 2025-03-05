from maya import cmds

selection = cmds.ls(sl=1)

# create a loop over each object in selection

for geo in selection:
    if cmds.listRelatives(geo)[0] in cmds.ls(et='mesh'):

        cmds.setAttr(geo + ".aiSubdivType", 1);
        cmds.setAttr(geo + ".aiSubdivIterations", 2);