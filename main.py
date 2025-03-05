from maya import cmds

class ArnoldSubdUI:
    '''
    A Maya tool for adjusting the Attribute Editor Arnold Subdivision tab for multiple objects simultaneously
    '''

    def __init__(self):
        #Initialize variables
        self.window_title = "Set Arnold Subdivision"
        self.tool_window = self.window_title.replace(" ", "_").casefold()
        self.selection = cmds.ls(sl=1)

        #Build UI
        self.window_cleaner()
        self.build_ui()

    def build_ui(self):
        """
        Constructs the user interface for the Batch Renderer tool.
        """
        self.tool_window = cmds.window(self.tool_window,
                                       title=self.window_title,
                                       widthHeight=(400, 300))
        cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

        self.mainLayout = cmds.columnLayout(w=250, h=150)

        #Title text
        cmds.text(label="Arnold Subdivisions",
                  w=250, h=50, fn="boldLabelFont",
                  bgc=(0.15,0.15,0.15))
        cmds.separator(h=10, style="none")

        self.rowLayout = cmds.rowColumnLayout( nc=3, cw= [(1,150),(2,50),(3,50)],
                                               columnOffset=[(1, "both", 5),
                                               (2, "both", 5), (3, "both", 5)])

        #Dropdown layout
        self.subOptionMenu = cmds.optionMenuGrp("subOptionMenu", label="Sub Type", cal=[1, "left"], cw=(1, 47))
        cmds.menuItem(label="none")
        cmds.menuItem(label="catclark")
        cmds.menuItem(label="linear")

        #Set catclark as default
        cmds.optionMenuGrp(self.subOptionMenu, e=1, sl=2)

        self.iterationNumbtext = cmds.text(label="Iterations", fn="plainLabelFont", align="left")
        self.iterationNumb     = cmds.intField("subNumb", minValue=0, maxValue=100, value=2, w=10)

        cmds.separator(h=10, style="none")

        self.subBtn = cmds.button(label = "Set Subdivisions",w=250, h=50, parent=self.mainLayout) #command=aiSubdivs

        #Display UI
        cmds.showWindow(self.tool_window)

    def window_cleaner(self):
        """
        Cleans up any existing UI window with the same name before creating a new one.
        """
        if cmds.window(self.tool_window, exists=True):
            cmds.deleteUI(self.tool_window)

    def set_subdiv_and_iterations(self):
        '''
        Loops over the selection and only applies changes on meshes (no cameras, lights,...)
        '''

        # Create a loop over each object in selection

        for geo in self.selection:
            if cmds.listRelatives(geo)[0] in cmds.ls(et='mesh'): #only use meshes
                cmds.setAttr(geo + ".aiSubdivType", 1);
                cmds.setAttr(geo + ".aiSubdivIterations", 2);

# Run the tool
ArnoldSubdUI()