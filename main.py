#Elise Bourgoignie
from maya import cmds

class ArnoldSubdUI:
    """
    A Maya tool for adjusting the Attribute Editor Arnold Subdivision tab for multiple objects simultaneously
    """

    def __init__(self):
        #Initialize variables
        self.window_title = "Set Arnold Subdivision"
        self.tool_window = self.window_title.replace(" ", "_").casefold()

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

        #Iteration input field
        self.iterationNumbtext = cmds.text(label="Iterations", fn="plainLabelFont", align="left")
        self.iterationNumb     = cmds.intField("iterationNumb", minValue=0, maxValue=100, value=2, w=10)

        cmds.separator(h=10, style="none")

        self.subBtn = cmds.button(label = "Set Subdivisions",w=250, h=50, parent=self.mainLayout,
                                  command=self.set_subdiv_and_iterations)

        #Display UI
        cmds.showWindow(self.tool_window)

    def window_cleaner(self):
        """
        Cleans up any existing UI window with the same name before creating a new one.
        """
        if cmds.window(self.tool_window, exists=True):
            cmds.deleteUI(self.tool_window)

    def set_subdiv_and_iterations(self, *args):
        """
        Loops over the selection and only applies changes to valid mesh objects.
        """

        #Catch selection at the moment of the button being activated
        self.selection = cmds.ls(sl=True, long=True)

        if not self.selection:
            cmds.warning("No objects selected. Please select one or more objects and try again.")
            return

        sub_type = cmds.optionMenuGrp(self.subOptionMenu, q=True, sl=True) - 1
        iteration_count = cmds.intField(self.iterationNumb, q=True, v=True)

        updated_objects = 0

        for obj in self.selection:
            shape = cmds.listRelatives(obj, shapes=True, fullPath=True)

            if shape and cmds.nodeType(shape[0]) == "mesh":
                try:
                    if cmds.attributeQuery("aiSubdivType", node=shape[0], exists=True):
                        cmds.setAttr(shape[0] + ".aiSubdivType", sub_type)
                        cmds.setAttr(shape[0] + ".aiSubdivIterations", iteration_count)
                        updated_objects += 1
                    else:
                        cmds.warning(f"{obj} does not have Arnold attributes. Skipping.")
                except Exception as e:
                    cmds.warning(f"Failed to set attributes for {obj}: {e}")

        if updated_objects > 0:
            cmds.inViewMessage(amg=f"<hl>{updated_objects} object(s) updated with new subdivision settings!</hl>",
                               pos="topCenter", fade=True)
        else:
            cmds.warning("No valid mesh objects found in the selection.")

# Run the tool
ArnoldSubdUI()