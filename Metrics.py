# -*- coding: utf-8 -*-
'''
Created on Jan 27, 2016

@author: souvik

This module is used to create the interfaces for Metrics and Metrics Factory which are used for instrumentation of code. 

For metrics to appear in the monitor portal the following attributes must be defined in the metrics 
1) ProgramName - The service for which the metrics are getting generated For e.g - CinderAPI
2) OperationName - "The sub component of the service. Typically if the service is an API , the subcomponent can be the specific method name(For e.g CreateVolume)"
3) RequestId - An id which uniquely identifies a request
4) marketPlace - Something that identifies the Scope and identity of the Service (can be used for both regions or availability zone)
5) EndTime - time it takes to end the request
6) Time - time taken by the request

Example Usage:
    Step 1:
        Create the metric object at start of a request
        metricsFactory = SomeMetricsFactoryImpl()
        metrics = new MetricsFactoryImpl().create_metrics()
        metrics.add_property("ProgramName", "CinderAPI")     // mandatory Params
        metrics.add_property("OperationName", "CreateVolume") // mandatory Params
        metrics.add_property("RequestId", "q311-r329-r302-jf2j-f92f-if93") // mandatory Params
        metrics.add_property("hostName", "sbs-cinderhost-1001") // mandatory Params
        metrics.add_property("marketPlace", "IDC1")    // mandatory Params
        metrics.add_property("accountId", "xxxxxxxxxxxxxxx") 
    
    Step 2: 
        Put this metrics object in a context, preferably request scoped
        requestScopeContext.putMetrics(metrics);
    
    Step 3:
        Retrieve the metrics object from the container and    
        ......
        Do some thing stupid... really stupid
        ........
        localMetricsReference = requestScopeContext.getMetrics("requestScopedMetrics");
        localMetricsReference.add_count("Success", 1)
        localMetricsReference.add_count("Failure", 0)
        localMetricsReference.add_count("Error", 0)
        localMetricsReference.add_count("Fault", 0)
        localMetricsReference.add_count("Retry", 0)

    Step 4:
        Close the metrics when done
        metrics.close()

    Any mutates after this will just not produce any effect.

Example Output: This is expected to have similar output file
    ===============================================================================
    StartTime=1453984418.7
    EndTime=2016-01-28 18:03:38
    Time=10 ms
    OperationName=CreateVolume
    HostName=souvik-HP-ProBook-450-G2
    PID=15115
    RequestId=q311-r329-r302-jf2j-f92f-if93
    ProgramName=CinderAPI
    AccountId=xxxxxxxxxxxxxxx
    MarketplaceId=IDC1
    Sample_Date_Field=1453984418.7
    Timing=DatebaseConnectionTime=500 ms,RetryWaitTime=1000 ms,
    Counters=Failure=0,Fault=0,Retry=0,Success=1,Error=0,
    EOE
    '''

from abc import ABCMeta

class Unit(object):
    __metaclass__ = ABCMeta
    """This prevents instantiation of the class since it is an interface
    """
    
    """ Unit Dimensions - TODO: need more work on this ..
    Looking for a suitable alternative from JavaWorld: http://jscience.org/api/javax/measure/unit/package-summary.html
    """
    SECONDS = "s"
    MILLIS = "ms"
    ONE = ""
    # TODO: Think of adding more metrics here

class Metrics(object):
    """ This is an interface for Metric Objects which are used to add metric attributes like properties, counters, datetime and time
    """
    __metaclass__ = ABCMeta
    """This prevents instantiation of the class since it is an interface
    """
    
    def add_property(self, name, value):
        """ Module to add properties to the metric object
    
        Args:
            name (string): Name of the Property
            value (string): Value fo the Property
    
        Example Usage:
            metrics.add_property("OperationName", "CreateVolume")
            metrics.add_property("RequestId", "q311-r329-r302-jf2j-f92f-if93")
            metrics.add_property("hostName", "sbs-cinderhost-1001")
            metrics.add_property("marketPlace", "IDC1")
        """
        pass


    def add_date(self, name, value):
        """ Module to add datetime objects to a metric class
    
        Args:
            name (string): Name of the DateTime object
            value (dateTime): value of the DateTime object
    
        Example Usage:
            metrics.add_date"startTime", datetime.datetime.now())  
            metrics.add_date("endTime", datetime.datetime.now()) 
        """
        pass

    def add_count(self, name, value):
        """ Module to add Counters to the metric object. The unit is always Count.ONE
        
        Args:
            name (string): Name of the Counter
            value (dateTime): Numerical Value of the counter
    
        Example Usage:
            metrics.add_count("Success", 1)
            metrics.add_count("Failure", 0)
            metrics.add_count("Error", 0)
            metrics.add_count("Fault", 0)
            metrics.add_count("Retry", 0)
        """
        pass

    def add_time(self, name, value, unit):
        """ Module to add dateTime of the metric object
        
        Args:
            name (string): Name of the DateTime object
            value (dateTime): numerical value in milliseconds
    
        Example Usage:
            startTime = datetime.datetime.now()
            Do some thing stupid... really stupid
            endTime = datetime.datetime.now()
            metrics.add_time("Time", startTime-endTime)
        """
        pass

    
    def close(self):
        """Module to close the metrics object where it wont accept anymore 
        values and it wont be able to modify the metric object
        """
        pass

class MetricsFactory(object):
    """ This is an interface factory method to create an instance of Metrics class
    """
    # TODO: This classes should not be instantiable.
    # But we need to solve this problem first.
    # metaclass conflict: the metaclass of a derived class must be a (non-strict)
    # subclass of the metaclasses of all its bases
    __metaclass__ = ABCMeta
    """This prevents instantiation of the class since it is an interface
    """
    
    def create_metrics(self):
        """ This method creates a metric instance
        """
        pass
    
