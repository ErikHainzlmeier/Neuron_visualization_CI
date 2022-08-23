
filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\CL_geom_v2\\Neurons\\"

for i in range (0,400):
    filename = filepath + "sweep" + str(i+1) + ".stl"
    print(filename)
    cmds.file(filename, i=True)