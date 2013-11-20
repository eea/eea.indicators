""" Event handlers
"""

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName


def syncWorkflowStateRelatedFigures(context, dest_state):
    """ Event handler
    """
    wftool = getToolByName(context, "portal_workflow")

    codes = context.get_codes()
    indcodes = codes and codes[-1] or "_missing_"
    comment = ("Automatic state change since related indicator (%s) "
               "has also changed state") % indcodes

    for ap in context.objectValues('AssessmentPart'):
        for figure in (o for o in ap.getRelatedItems()
                       if o.portal_type in ("EEAFigure","DavizVisualization")):
            figState = wftool.getInfoFor(figure, 'review_state')
            
            # ignore already published figures
            if (figState != dest_state and figState != 'published'):

                # get possible transitions for object in current state

                workflow = wftool.getWorkflowsFor(figure)[0]
                transitions = workflow.transitions
                available_transitions = [transitions[i['id']] for i in
                                            wftool.getTransitionsFor(figure)]

                to_do = [k for k in available_transitions
                         if k.new_state_id == dest_state]

                if not to_do:
                    err = """
The figure %s has an incompatible worklfow state. Please contact web admin. 
""" % figure.absolute_url()
                    IStatusMessage(context.REQUEST).add(err, 'warn')
                    raise ValueError(err)

                # find transition that brings to the state of parent object
                for item in to_do:
                    workflow.doActionFor(figure, item.id, comment=comment)
                    figure.reindexObject()
                    break


def handle_assessment_state_change(context, event):
    """ Event handler
    """
    dest_state = event.workflow.transitions[event.action].new_state_id

    if dest_state in ['published', 'visible']:
        syncWorkflowStateRelatedFigures(context, dest_state)


def handle_specification_state_change(context, event):
    """ Event handler to reindex children assessments
        to update their readiness
    """
    catalog = getToolByName(context, 'portal_catalog')
    objs = context.objectValues()
    for obj in objs:
        catalog.reindexObject(obj, idxs=[], update_metadata=True)


def handle_policyquestion_modification(context, event):
    """ Event handler to reindex parent specification
        to update their readiness
    """
    catalog = getToolByName(context, 'portal_catalog')
    spec = context.aq_parent
    catalog.reindexObject(spec, idxs=[], update_metadata=True)


def handle_assessmentpart_modification(context, event):
    """ Event handler to reindex parent assessment
        to update their readiness
    """
    catalog = getToolByName(context, 'portal_catalog')
    assessment = context.aq_parent
    catalog.reindexObject(assessment, idxs=[], update_metadata=True)


def handle_reindex_children(context, event):
    """ Event handler to reindex all children of an
        indicator specification
    """
    catalog = getToolByName(context, 'portal_catalog')
    objs = context.objectValues()
    for obj in objs:
        catalog.reindexObject(obj)

