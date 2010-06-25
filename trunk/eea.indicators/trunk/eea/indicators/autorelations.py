from zope.component import getMultiAdapter                                                                                                                              


class DatasetsFromFigures(object):                                                                                                                                      
    """ Return datasets used in the latest figures of an assessment for a specification.                                                                                
    """                                                                                                                                                                 
    def __init__(self, context):                                                                                                                                        
        self.context = context                                                                                                                                          
        self.request = getattr(self.context, 'REQUEST', None)                                                                                                           
                                                                                                                                                                        
    def __call__(self, **kwargs):                                                                                                                                       
        """ Return all the related data sets from the assessments figures.                                                                                              
        """                                                                                                                                                             
        #get my published assessments                                                                                                                                                                                                                                                      
        assessments = getMultiAdapter((self.context, self.request),                                                                                                     
                                   name=u'assessment_versions')                                                                                                         
        all_assessments = assessments()                                                                                                                                 
        published_assessments = all_assessments['published']                                                                                                            
        if len(published_assessments) > 0 :                                                                                                                             
            latest_assessment = published_assessments[-1]                                                                                                               
        else:                                                                                                                                                           
            latest_assessment = None                                                                                                                                    
                                                                                                                                                                        
        #get the figures for each assessment part, we can use related_items view
        figs=[]                                                                                                                                                         
        if latest_assessment:                                                                                                                                           
            #take the key part                                                                                                                                          
            part = latest_assessment.objectValues('AssessmentPart')[-1]                                                                                                 
            related_items = getMultiAdapter((part, self.request),                                                                                                       
                                   name=u'related_items')                                                                                                               
            figs = related_items('EEAFigures')                                                                                                                          
                                                                                                                                                                        
        #TODO: get any related data on each figure                                                                                                                      
        return [('Data used in figures',figs),                                                                                                                          
                ('published assessments',published_assessments),] 

