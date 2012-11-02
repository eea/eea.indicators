"""Integration with eea.daviz
"""

from Products.Five.browser import BrowserView


        #mutator = queryAdapter(self.context, IVisualizationConfig)
        #config = ''
        #for view in mutator.views:
            #if (view.get('chartsconfig')):
                #config = view.get('chartsconfig')

        #if config == "":
            #return []

        #return config['charts']

class SetDavizChart(BrowserView):
    """Edit the chart for a daviz presentation that's set as related
    """

    def __call__(self):
        uid = self.request.form.get("vizualization_uid")
        chart = self.request.form.get("chart")

        annot = self.context.__annotations__['DAVIZ_CHARTS']
        annot[uid.strip()] = None
        
        import pdb; pdb.set_trace()
        return "done"
