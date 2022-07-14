
cmds.group(em=True, name='nodes')
name1 = 1
cmds.group(em=True, name='neuron' + str(name1), parent='nodes')

for i in range(5):
    sphere1 = cmds.polySphere(r=0.3, name='mySphere#')

    cmds.parent(sphere1[0], 'neuron1')