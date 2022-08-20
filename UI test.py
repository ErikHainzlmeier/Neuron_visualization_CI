def create_ui():
    window = cmds.window(title="Model Settings", widthHeight=(200, 500))

    cmds.columnLayout(adjustableColumn=True )
    cmds.rowLayout(numberOfColumns=2, columnAttach=(1, 'right', 0), adjustableColumn=2)

    cmds.text(label='Path')
    path_input = cmds.textField()



    cmds.setParent('..')
    cmds.separator(height = 30)
    cmds.setParent('..')
    cmds.rowLayout(adjustableColumn=1)
    cmds.button(label='Build model', command="run_ui(\"" + path_input + "\", \"" + str(a) + "\")", bgc=[0.4, 0.65, 0.2])

    cmds.showWindow(window)

def run_ui(path_input, a):
    path = cmds.textField(path_input, query=True, text=True)
    print(path)
    cmds.deleteUI(window, window=True)
    main()


def main():

    print("success!!!")

create_ui()


