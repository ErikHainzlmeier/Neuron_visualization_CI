
filepath = "C:\\Users\\Rafael\\Desktop\\praktikum bioanaloge\\CL_geom_v2\\Neurons\\"

for i in range (150, 170):
    filename = filepath + "sweep" + str(i+1) + ".fbx"
    cmds.file(filename, i=True)



# create new shader and assign a color to it
sweep_shader = cmds.shadingNode('aiStandardSurface', asShader=1, name='ShaderSweeps')
cmds.setAttr((sweep_shader + '.baseColor'), 0.15, 0.3, 0.5, type='double3')

cmds.select("sweeps", hierarchy=True)
cmds.hyperShade(a=sweep_shader)
cmds.select(clear=True)

