'''
Created on Jan 27, 2016

@author: souvik
'''
from AbstractMetrics import AbstractMetrics, AbstractMetricsFactory 

class NullMetrics(AbstractMetrics):
    ''' This is a null metrics object which just conditionally flushes output to console. To be used for unit testings or when service metrics needs to be disabled.
    '''

    def __init__(self, display_metric_to_console):
        '''
        Constructor
        '''
        super(NullMetrics, self).__init__()
        self.__display_metric_to_console = display_metric_to_console
    
    def _initialize_metrics(self):
        ''' Does nothing for NullMetrics
        '''
        pass
    
    def _flush_metrics(self):
        ''' This just flushes out the Metric object 
        '''
        if (self.__display_metric_to_console):
            print self.__str__()
        
class NullMetricsFactory(AbstractMetricsFactory):
    ''' Metrics factory to create null metrics
    '''
    
    def __init__(self):
        super(NullMetricsFactory, self).__init__()
        self.__display_metric_to_console = False
        
    def with_display_metric_to_console(self, display_metric_to_console):
        self.__display_metric_to_console = display_metric_to_console
        return self
    
    def create_metrics(self):
        metrics = NullMetrics(self.__display_metric_to_console)
        self._add_metric_attributes(metrics)
        return metrics  

        