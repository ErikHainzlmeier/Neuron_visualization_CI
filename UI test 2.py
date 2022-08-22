class ui_settings(object):

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

        # Title
        cmds.text(self.title)
        cmds.separator(height=20)

        # measurement settings
        cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 145), (2, 250)])
        cmds.text(" -Measurement Settings:")
        cmds.text(" ")
        cmds.text(label='Measurements Filepath:')
        self.filepath = cmds.textField()
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 145), (2, 70)])
        cmds.text("Measurement Stepsize:")
        self.measur_stepsize = cmds.intField(minValue=1, maxValue=1000, value=1)
        cmds.text(" ")
        cmds.text(" ")
        cmds.text(" ")
        cmds.text(" ")

        # Model specifications
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

        # measurement steps
        # cmds.text(" -Cochlea Structures:")
        # cmds.text(" ")
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 70), (2, 75), (3, 70)])
        cmds.text("Cochlea:")
        cmds.text("Import: ", align='right')
        self.import_cochlea = cmds.checkBox(label=' ')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.cochlea_transparency = cmds.floatSliderGrp(field=True, label='Transparency:', minValue=0, maxValue=1,
                                                        value=0.8, columnAlign=[1, 'right'])
        self.cochlea_color = cmds.colorSliderGrp(label='Colour:', rgb=(0.7, 0.7, 0.7), columnAlign=[1, 'right'])

        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 70), (2, 75), (3, 70)])
        cmds.text("Tube:")
        cmds.text("Import: ", align='right')
        self.import_tube = cmds.checkBox(label=' ')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.tube_transparency = cmds.floatSliderGrp(field=True, label='Transparency:', minValue=0, maxValue=1,
                                                     value=0.9, columnAlign=[1, 'right'])
        self.tube_color = cmds.colorSliderGrp(label='Colour:', rgb=(0.7, 0.7, 0.7), columnAlign=[1, 'right'])

        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=3, columnAttach=(1, 'left', 0), columnWidth=[(1, 70), (2, 75), (3, 70)])
        cmds.text("Nerve:")
        cmds.text("Import: ", align='right')
        self.import_nerve = cmds.checkBox(label=' ')
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.nerve_transparency = cmds.floatSliderGrp(field=True, label='Transparency:', minValue=0, maxValue=1,
                                                      value=0, columnAlign=[1, 'right'])
        self.nerve_color = cmds.colorSliderGrp(label='Colour:', rgb=(0.5, 0.7, 1), columnAlign=[1, 'right'])
        cmds.text(" ")
        cmds.text(" ")

        # Animation settings
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 145), (2, 70)])
        cmds.text(" -Animation Settings:")
        cmds.text(" ")
        cmds.setParent('..')
        cmds.rowColumnLayout(numberOfColumns=1, columnAttach=(1, 'left', 0), columnWidth=[(1, 395)])
        self.light_intensity = cmds.floatSliderGrp(field=True, label='Light Intensity:', minValue=0, maxValue=1,
                                                   value=0,
                                                   columnAlign=[1, 'right'])
        self.camera_speed = cmds.floatSliderGrp(field=True, label='Camera Speed:', minValue=0, maxValue=1000, value=100,
                                                columnAlign=[1, 'right'])

        # Build model button
        cmds.setParent('..')
        cmds.separator(height=30)
        cmds.button(label='Build Model', bgc=[0.4, 0.65, 0.2], command=self.run_variables)

        # display new window
        cmds.showWindow()

    def run_variables(self, *args):
        path = cmds.textField(self.filepath, query=True, text=True)
        measur_stepsize = cmds.intField(self.measur_stepsize, query=True, value=True)
        firstNeur = cmds.intField(self.firstNeur, query=True, value=True)
        lastNeur = cmds.intField(self.lastNeur, query=True, value=True)
        neur_stepsize = cmds.intField(self.neur_stepsize, query=True, value=True)
        import_cochlea = cmds.checkBox(self.import_cochlea, query=True, value=True)
        cochlea_transparency = cmds.floatSliderGrp(self.cochlea_transparency, query=True, value=True)
        cochlea_color = cmds.colorSliderGrp(self.cochlea_color, query=True, rgbValue=True)
        import_tube = cmds.checkBox(self.import_tube, query=True, value=True)
        tube_transparency = cmds.floatSliderGrp(self.tube_transparency, query=True, value=True)
        tube_color = cmds.colorSliderGrp(self.tube_color, query=True, rgbValue=True)
        import_nerve = cmds.checkBox(self.import_nerve, query=True, value=True)
        nerve_transparency = cmds.floatSliderGrp(self.nerve_transparency, query=True, value=True)
        nerve_color = cmds.colorSliderGrp(self.nerve_color, query=True, rgbValue=True)
        light_intensity = cmds.floatSliderGrp(self.light_intensity, query=True, value=True)
        camera_speed = cmds.floatSliderGrp(self.camera_speed, query=True, value=True)

        main(path, measur_stepsize, firstNeur, lastNeur, neur_stepsize, import_cochlea, cochlea_transparency,
                  cochlea_color, import_tube, tube_transparency, tube_color, import_nerve, nerve_transparency,
                  nerve_color, light_intensity, camera_speed)
        cmds.deleteUI(self.window, window=True)


def main(path, measur_stepsize, firstNeur, lastNeur, neur_stepsize, import_cochlea, cochlea_transparency,
                  cochlea_color, import_tube, tube_transparency, tube_color, import_nerve, nerve_transparency,
                  nerve_color, light_intensity, camera_speed):
    print("this is the start of the program")



ui_settings()
