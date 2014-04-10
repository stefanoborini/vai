class SideRulerController(object):
    def __init__(self, side_ruler, view_model):
        self._side_ruler = side_ruler
        self._view_model = view_model
        self._view_model.documentPosChanged.connect(self.updateRange)

    def updateRange(self):
        top_pos = self._view_model.documentPosAtTop()
        self._side_ruler.setStart(top_pos.row)




