cameraName = cmds.camera()
cameraShape = cameraName[1]
aimLoc = 'mySphere18'
cmds.aimConstraint(aimLoc, cameraName[0], aimVector=(0,0,-1))
cmds.setAttr(cameraName[0]+".scaleY", -1)
#cmds.viewPlace(cameraName[0] )