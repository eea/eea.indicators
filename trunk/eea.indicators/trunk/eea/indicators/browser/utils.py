from Products.Five import BrowserView
import logging

class Sorter(BrowserView):
    """Sort objects inside an ordered folder based on new ids"""

    def __call__(self):
        new = self.request.form.get('order')
        old = self.context.objectIds()

        for i, id in enumerate(new):
            old_i = old.index(id)
            if old_i != i:
                self.context.moveObjectToPosition(id, i)
                #logging.info("Moved %s from position %s to %s", id, old_i, i)

        return "<done />"
