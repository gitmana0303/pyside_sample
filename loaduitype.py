import maya.cmds as cmds
import pysideuic
import xml.etree.ElementTree as xml
from cStringIO import StringIO
from PySide import QtGui

#-------------------------------------------------------------------------------
# load ui file (generate window parent classes)
#-------------------------------------------------------------------------------
class LoadUiType(object):
    def __init__(self):
        pass

    def build(self, uiFile):
        'load a .ui file in memory'
        parsed = xml.parse(uiFile)
        widget_class = parsed.find('widget').get('class')
        form_class = parsed.find('class').text
     
        with open(uiFile, 'r') as f:
            o = StringIO()
            frame = {}
             
            pysideuic.compileUi(f, o, indent=0)
            pyc = compile(o.getvalue(), '<string>', 'exec')
            exec pyc in frame
             
            # Fetch the base_class and form class based on their type
            # in the xml from designer
            form_class = frame['Ui_%s'%form_class]
            base_class = eval('QtGui.%s'%widget_class)
     
        return form_class, base_class


#----------------------------------------------------
if __name__ == '__main__':
#----------------------------------------------------
    LUT = LoadUiType()
    form_class, base_class = LUT.build(r"C:\test.ui")