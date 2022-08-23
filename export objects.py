filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\CL_geom_v2\\Neurons\\"

for i in range(0, 400):
    objName = 'sweep' + str(i+1)
    filename = filepath + objName
    cmds.select(objName)
    cmds.file(filename, force = True, type = "FBX Export", exportSelected = True)


#FBX ist flexibel, aber erstellt einen neuen Shader für jedes Objekt
#maya binary klein und schnell
#maya Ascii erstellt shader für jedes neuron
#stl ist schnell und klein, aber nicht schön
#usd geht schnell, aber es importiert dann nichts xD