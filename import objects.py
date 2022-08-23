
filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\CL_geom_v2\\test\\"

for i in range (150, 170):
    filename = filepath + "sweep" + str(i+1) + ".fbx"
    cmds.file(filename, i=True)

cmds.select("sweeps", hierarchy=True)

