'''
Created on Jan 29, 2016

@author: souvik
'''
from metrics.ThreadLocalMetrics import ThreadLocalMetrics, ThreadLocalMetricsFactory
from metrics.Metrics import Unit
from oslo_log import log as logging
from time import time
LOG = logging.getLogger(__name__)

'''
This decorator wraps around any method and captures latency around it. If the parameter 'report_error' is set to True
then it also emits metrics on whether the method throws an exception or not
'''
class ReportMetrics(object):
    '''
    @:param metric_name This variable declares what is the latency of an afforsaid sub component call.
    @:param report_error If this is set to True it adds an error counter to 1 if there is an error and 0 if there are no
     error
    '''
    def __init__(self, metric_name, report_error = False):
        self.__metric_name = metric_name
        self.__report_error = report_error
    def __call__(self, function):
        def metrics_wrapper(*args, **kwargs):
            start_time = time()
            error = 0
            try:
                return function(*args, **kwargs)
            except Exception as e:
                LOG.error("Exception while executing " + function.__name__)
                error = 1
                raise e
            finally:
                end_time = time()
                try:
                    metrics = ThreadLocalMetrics.get()
                    metric_time = self.__metric_name + "_time"
                    metrics.add_time(metric_time, int((end_time - start_time)*1000), Unit.MILLIS)
                    if self.__report_error == True:
                        metric_error = self.__metric_name + "_error"
                        metrics.add_count(metric_error, error)
                except AttributeError as e:
                    LOG.exception("No threadlocal metrics object: %s", e)

        return metrics_wrapper

class MetricUtil(object):
    '''
    Metric Utility class to put and fetch request add_timescoped metrics in cinder api
    '''
    METRICS_OBJECT = "metrics_object"
    def __init__(self):
        '''
        Constructor for Metric Utils. 
        '''

    '''
    This method takes in a service log path and program name (like CinderAPI, EC2API layer etc) and initializes
    the thread local metrics if it has not already been initiatized before in the same request
    '''
    def initialize_thread_local_metrics(self, use_zmq, service_log_path, program_name):
        try:
            metrics = self.fetch_thread_local_metrics()
        except AttributeError:
            metrics = ThreadLocalMetricsFactory(use_zmq,service_log_path).with_marketplace_id(self.get_marketplace_id())\
                            .with_program_name(program_name).create_metrics()
        return metrics

    '''
    This method fetches the current thread local metrics from thread local
    '''
    def fetch_thread_local_metrics(self):
        return ThreadLocalMetrics.get()

    '''
    This method fetches the market place id
    '''
    def get_marketplace_id(self):
        # TODO:Get this from the config when we have multiple zones/regions
        return "IDC1"

    '''
    Closing the metrics emits the metrics in logs
    '''
    def closeMetrics(self, request):
        metrics = self.fetch_thread_local_metrics()
        metrics.close()

    '''
    Add the following metric name to the timing metrics taking the difference between start_time and end_time
    '''
    def report_timing_metric_utc_time(self, metric_name, end_time, start_time):
        metrics = self.fetch_thread_local_metrics()
        delta = end_time - start_time
        seconds = delta.seconds
        microseconds  = delta.microseconds
        milliseconds = int(microseconds/1000 + seconds*1000)
        metrics.add_time(metric_name, milliseconds, Unit.MILLIS)
