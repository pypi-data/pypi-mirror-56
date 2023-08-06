#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Producer and Consumer messages.

    This library do this:

    Use Redis or Kafka as queue or stream data

"""
__author__ = "Lennin Caro"
__copyright__ = "Copyright 2018, Syn Client (Redis or Kafka as Queue)"
__credits__ = ["Lennin Caro"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Lennin Caro"
__email__ = "renjin25@gmail.com"
__status__ = "Production"
from typing import List, Dict, Tuple, Set, TypeVar
from syn_client.core.utils import SysInfo
from confluent_kafka.cimpl import KafkaError
from syn_client.core.kafka_client_len import Consumer as SKConsumer, Producer as SKProducer, Admin as SKAdmin, Log as SKLog
from syn_client.core.redis_client_len  import Consumer as SRConsumer, Producer as SRProducer, Log as SRLog
import types

       
class SynKafka(object):

    def __init__(self, *args, **kwargs):
        pass

    class Consumer(SKConsumer):
        def __init__(self, *args, **kwargs): 
            super().__init__(**kwargs)

        @staticmethod    
        def on_error(error: KafkaError): 
            print('KafkaError: %s', error.str())

        @staticmethod
        def on_commit(error: KafkaError, partitions):
            pass

        @staticmethod
        def on_stats(stats_json_str):
            pass

        @staticmethod
        def on_assignment(consumer, partitions):
            pass
    
    class Producer(SKProducer):
        def __init__(self, *args, **kwargs): 
            super().__init__(**kwargs)

        @staticmethod
        def on_delivery_callback(err, msg):
            pass

    class Admin(SKAdmin):
        def __init__(self, *args, **kwargs): 
            super().__init__(**kwargs)

    class Log(SKLog):
        def __init__(self, *args, **kwargs): 
            super().__init__(**kwargs)
    
class SynRedis(object):

    def __init__(self, *args, **kwargs):
        pass

    class Consumer(SRConsumer):
        def __init__(self, *args, **kwargs): 
            super().__init__(**kwargs) 
    
    class Producer(SRProducer):
        def __init__(self, *args, **kwargs): 
            super().__init__(**kwargs) 
    
    class Log(SRLog):
        def __init__(self, *args, **kwargs): 
            super().__init__(**kwargs)