'''
Created on Jan 27, 2016

@author: souvik


################## This is just a test class for demonstration purpose only. Remove this class ASAP #############################
''' 
from metrics.NullMetrics import NullMetricsFactory
from metrics.ThreadLocalMetrics import ThreadLocalMetricsFactory
from metrics.Metrics import Metrics, Unit
from datetime import datetime
from time import time, sleep

#from time import time
#from socket import socket

if __name__ == '__main__':
    
    #metricsFactory = ThreadLocalMetricsFactory("/tmp/service_log").with_account_id("xxxxxxxxxxxxxxx").with_marketplace_id("IDC1").with_program_name("CinderAPI").with_operation_name("CreateVolume");
    metricsFactory = NullMetricsFactory().with_display_metric_to_console(True).with_account_id("xxxxxxxxxxxxxxx").with_marketplace_id("IDC1").with_program_name("CinderAPI").with_operation_name("CreateVolume");
    
    i = 0                         
    while (i<100):
        metrics =  metricsFactory.create_metrics();
        
        metrics.add_property("RequestId", "q311-r329-r302-jf2j-f92f-if93")
        metrics.add_date("Sample_Date_Field",  time())
        metrics.add_count("Success", 1)
        metrics.add_count("Failure", 0)
        metrics.add_count("Error", 0)
        metrics.add_count("Fault", 0)
        metrics.add_count("Retry", 0)
        metrics.add_time("DatebaseConnectionTime", 500, Unit.MILLIS)
        metrics.add_time("RetryWaitTime", 1, Unit.SECONDS)
        
        sleep(0.01)
        metrics.close()
        i = i+1
        #print datetime().now()