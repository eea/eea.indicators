from Products.CMFCore.utils import getToolByName
from StringIO import StringIO

def publishRelatedFigures(statechange, **kw):
    out = StringIO()
    context = statechange.object
    if not context.portal_type == "Assessment":
        return

    cat = getToolByName(context, "portal_catalog")
    wf  = getToolByName(context, "portal_workflow")

    print >> out, "START"
    fignr = 0
    pubo = context
    parentState = wf.getInfoFor(pubo, 'review_state')
    #pubo.reindexObject()
    #field = pubo.getField('rights')
    #value = field.getAccessor(pubo)()

    if parentState == 'published':
          for ass in pubo.objectValues('AssessmentPart'): 
             for ob in ass.getRelatedItems():
                if ob.portal_type == 'EEAFigure':
                    #figs=cat.searchResults({ 'meta_type' : ['EEAFigure'], 'id':ob.id})
                    figState = wf.getInfoFor(ob, 'review_state')
                    if figState != 'published':
                        fignr += 1
                        indcodes = str(pubo.get_codes()[1])
                        print >> out, 'INDICATOR: ' + str(pubo.get_codes())
                        print >> out, pubo.absolute_url()
                        print >> out, parentState
                        print >> out, 'FIGURE:'
                        print >> out, ob.id
                        print >> out, ob.absolute_url()
                        print >> out, figState
                        # get possible transitions for object in current state
                        figfiles = ob.objectValues('EEAFigureFile')
                        figfiles.append(ob)
                        for obj in figfiles:
                           actions = wf.getActionsFor(obj)
                           transitions = []
                           for item in actions:
                              if item.has_key('transition'):
                                   transitions.append(item['transition'])
                           print >> out, str(transitions)
                           # find transition that brings us to the state of parent object
                           for item in transitions:
                               if item.new_state_id == parentState:
                                    print >> out, obj.meta_type
                                    print >> out, obj.absolute_url()
                                    print >> out, 'transition to publish found!:'+ str(item)
                                    mycomment = "automatically published since related indicator (" + indcodes + ") is also published"
                                    print >> out, mycomment
                                    wf.doActionFor(obj, item.id, comment=mycomment)
                                    obj.reindexObject()

    print >> out, "tot nr figures still not published in published ind:" + str(fignr)
    out.seek(0)

    return out.read()


def after_publish(statechange, **kw):
    context = statechange.object
    wftool = getToolByName(context, 'portal_workflow')
    wf = wftool['indicators_workflow']

    print "Doing send workflow"
    wf['scripts']['sendWorkflowEmail'](statechange, **kw)
    print "Doing publish related figures workflow"
    wf['scripts']['publishRelatedFigures'](statechange, **kw)

