import tpDccLib as tp

import artellapipe.register
from artellapipe.core import toolbox


class HoudiniToolBox(toolbox.ToolBox, object):
    def __init__(self, project, parent=None):
        if parent is None:
            parent = tp.Dcc.get_main_window()
        super(HoudiniToolBox, self).__init__(project=project, parent=parent)


artellapipe.register.register_class('ToolBox', HoudiniToolBox)
