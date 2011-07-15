from itertools import chain
from Products.CMFCore.utils import getToolByName


def syncWorkflowStateRelatedFigures(context, dest_state):
    """ Event handler"""
    wftool = getToolByName(context, "portal_workflow")

    codes = context.get_codes()
    indcodes = codes and codes[-1] or "_missing_"
    comment = ("Automatically published since related indicator (%s) "
               "is also published") % indcodes

    for ap in context.objectValues('AssessmentPart'):
        for ob in filter(lambda o:o.portal_type=="EEAFigure", 
                ap.getRelatedItems()):
            figState = wftool.getInfoFor(ob, 'review_state')
            if figState != dest_state:

                # get possible transitions for object in current state
                for obj in chain([ob], ob.objectValues('EEAFigureFile')):
                    workflow = wftool.getWorkflowsFor(obj)[0]
                    transitions = workflow.transitions

                    # find transition that brings to the state of parent object
                    for item in filter(lambda i:i.new_state_id == dest_state, 
                            transitions.objectValues()):
                        workflow.doActionFor(obj, item.id, comment=comment)
                        obj.reindexObject()
                        break


def handle_assessment_state_change(context, event):
    """ Event handler"""
    dest_state = event.workflow.transitions[event.action].new_state_id

    if dest_state in ['published', 'visible']:
        syncWorkflowStateRelatedFigures(context, dest_state)

    if dest_state in ['visible', 'published_eionet']:
        context.allowDiscussion('off')
    else:
        context.allowDiscussion('on')


def handle_specification_state_change(context, event):
    """ Event handler"""
    #reindex children assessments to update their readiness
    catalog = getToolByName(context, 'portal_catalog')
    catalog.reindexObject(context, idxs=[], update_metadata=True)


def handle_policyquestion_modification(context, event):
    """ Event handler"""
    #reindex parent specification to update their readiness
    catalog = getToolByName(context, 'portal_catalog')
    catalog.reindexObject(context, idxs=[], update_metadata=True)


def handle_assessmentpart_modification(context, event):
    """ Event handler"""
    #reindex parent assessment to update their readiness
    catalog = getToolByName(context, 'portal_catalog')
    catalog.reindexObject(context, idxs=[], update_metadata=True)
