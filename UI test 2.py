class MR_Window(object):

    # constructor
    def __init__(self):
        self.window = "MR_Window"
        self.title = "Settings"
        self.size = (395, 600)

        # close old window is open
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        # create new window
        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)

        cmds.columnLayout(adjustableColumn=True)

        #Title
        cmds.text(self.title)
        cmds.separator(height=20)

        #measurement settings
        cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 145), (2, 250)])
        cmds.text(" -Measurement Settings:")
        cmds.text(" ")
        cmds.text(label ='Measurements Filepath:')
        self.filepath = cmds.textField()
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 145), (2, 70)])
        cmds.text("Measurement Stepsize:")
        self.measur_stepsize = cmds.intField(minValue=0, maxValue=1000, value=1)
        cmds.text(" ")
        cmds.text(" ")
        cmds.text(" ")
        cmds.text(" ")

        #Model specifications
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 145), (2, 70)])
        cmds.text(" -Model Specicifactions:")
        cmds.text(" ")
        cmds.text("First Neuron:")
        self.firstNeur = cmds.intField(minValue=0, maxValue=399, value=0)
        cmds.text("Last Neuron:")
        self.lastNeur = cmds.intField(minValue=1, maxValue=400, value=400)
        cmds.text("Step Size:")
        self.neur_stepsize = cmds.intField(minValue=1, maxValue=400, value=1)

        #measurement steps
        #cmds.text(" -Cochlea Structures:")
        #cmds.text(" ")
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 70), (2, 75), (3, 70)])
        cmds.text("Cochlea:")
        cmds.text("Import: ", align='right')
        self.import_cochlea = cmds.checkBox(label=' ')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.cochlea_transparency = cmds.floatSliderGrp(field=True, label='Transparency:', minValue=0, maxValue=1, value=0.8, columnAlign=[1, 'right'])
        self.cochlea_color = cmds.colorSliderGrp(label='Colour:', rgb=(0.7, 0.7, 0.7),columnAlign=[1, 'right'])

        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 70), (2, 75), (3, 70)])
        cmds.text("Tube:")
        cmds.text("Import: ", align='right')
        self.import_tube = cmds.checkBox(label=' ')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.cubeSubdivs = cmds.floatSliderGrp(field=True, label='Transparency:', minValue=0, maxValue=1, value=0.9, columnAlign=[1, 'right'])
        self.tube_color = cmds.colorSliderGrp(label='Colour:', rgb=(0.7, 0.7, 0.7),columnAlign=[1, 'right'])

        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 70), (2, 75), (3, 70)])
        cmds.text("Nerve:")
        cmds.text("Import: ", align='right')
        self.import_nerve = cmds.checkBox(label=' ')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.cubeSubdivs = cmds.floatSliderGrp(field=True, label='Transparency:', minValue=0, maxValue=1, value=0, columnAlign=[1, 'right'])
        self.nerve_color = cmds.colorSliderGrp(label='Colour:', rgb=(0.5, 0.7, 1),columnAlign=[1, 'right'])
        cmds.text(" ")
        cmds.text(" ")


        #Animation settings
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 145), (2, 70)])
        cmds.text(" -Animation Settings:")
        cmds.text(" ")
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.light_intensity = cmds.floatSliderGrp(field=True, label='Light Intensity:', minValue=0, maxValue=1, value=0,
                                               columnAlign=[1, 'right'])
        self.camera_speed = cmds.floatSliderGrp(field=True, label='Camera Speed:', minValue=0, maxValue=1000, value=100,
                                               columnAlign=[1, 'right'])


        #Build model button
        cmds.setParent('..')
        cmds.separator(height=30)
        cmds.button(label='Build Model', bgc=[0.4, 0.65, 0.2], command=self.run_variables())

        # display new window
        cmds.showWindow()

    def run_variables(self, *args):
        path = cmds.textFieldGrp(self.filepath, query=True, text=True)

        measurement_stepsize = cmds.intField(self.measur_stepsize, query=True)

        width = cmds.floatFieldGrp(self.firstNeur, query=True, value1=True)
        height = cmds.floatFieldGrp(self.lastNeur, query=True, value2=True)
        depth = cmds.floatFieldGrp(self.stepsize, query=True, value3=True)

        subdivs = cmds.intSliderGrp(self.cubeSubdivs, query=True, value=True)

        print("path:", path)
        print("measurement stepsize:", measurement_stepsize)

myWindow = MR_Window()