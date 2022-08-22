filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\CL_geom_v2\\Neurons\\"

for i in range(400):
    objName = 'sweep' + str(i+1)
    filename = filepath + objName
    cmds.select(objName)
    cmds.file(filename, force = True, options = "v = 0", type = "mayaBinary", exportSelected = True)