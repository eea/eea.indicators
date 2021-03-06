""" Event handlers
"""

from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName


def syncWorkflowStateRelatedFigures(context, dest_state):
    """ Event handler
    """
    wftool = getToolByName(context, "portal_workflow")

    codes = context.get_codes()
    indcodes = codes[-1] if codes else "_missing_"
    comment = ("Automatic state change since related indicator (%s) "
               "has also changed state") % indcodes

    for ap in context.objectValues('AssessmentPart'):
        for figure in (o for o in ap.getRelatedItems()
                       if o.portal_type in ("EEAFigure", "DavizVisualization",
                                            "GIS Application")):
            figState = wftool.getInfoFor(figure, 'review_state')

            # ignore already published figures
            if figState in (dest_state, 'published'):
                return

            # get possible transitions for object in current state
            workflow = wftool.getWorkflowsFor(figure)[0]
            transitions = workflow.transitions
            for transition in wftool.getTransitionsFor(figure):
                tid = transition.get('id')
                tob = transitions.get(tid)
                if not tob:
                    continue

                if tob.new_state_id != dest_state:
                    continue

                figure.setEffectiveDate(context.getEffectiveDate())
                workflow.doActionFor(figure, tid, comment=comment)
                figure.reindexObject()
                break
            else:
                # State not changed
                context_state = wftool.getInfoFor(
                    context, 'review_state', 'UNKNOWN')
                err = """
                    <p>The related figure %s cannot reach the destination
                       worklfow state <strong>%s</strong>.</p>
                    <p>You need to change the workflow state of this figure
                       to a state that has a transition to
                       <strong>%s</strong>.</p>
                    """ % (figure.absolute_url(), dest_state, context_state)
                IStatusMessage(context.REQUEST).add(err, 'error')
                raise ValueError(err)


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
