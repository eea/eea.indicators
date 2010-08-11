from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from StringIO import StringIO

import transaction
import logging
logger = logging.getLogger('eea.indicators')


class MigrateToOneStateWorkflow(BrowserView):
    """Update the role mappings for a set of determined content types"""

    wf = None

    def _update_ob(self, brain):
        ob = brain.getObject()
        try:
            self.wf.updateRoleMappingsFor(ob)
        except Exception, e:
            pass
        ob.reindexObject()  #idxs=['allowedRolesAndUsers']
        logging.info("Reindexed %s", ob)

    def __call__(self):

        types = (
                "AssessmentPart", 
                "ExternalDataSpec", 
                "MethodologyReference", 
                "PolicyDocumentReference", 
                "PolicyQuestion", 
                "RationaleReference", 
                "WorkItem", 
                )
        wf_name = "one_state_workflow"
        
        out = StringIO()

        wftool = getToolByName(self.context, 'portal_workflow')
        catalog = getToolByName(self.context, 'portal_catalog')
        self.wf = wftool[wf_name]

        for type_ in types:
            i = 0
            res = catalog.searchResults(portal_type=type_)
            for ob in res:
                self._update_ob(ob)
                i += 1
                if (i % 20) == 0:
                    transaction.commit()

            msg = "Updated %s of type %s" % (len(res), type_)
            logging.info(msg)
            print >> out, msg

        out.seek(0)
        return out.read()
