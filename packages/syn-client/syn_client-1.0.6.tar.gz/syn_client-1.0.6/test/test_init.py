#!/usr/bin/python3
# -*- coding: utf-8 -*-

       
from typing import List, Dict, Tuple, Set, TypeVar
from core.utils import SysInfo
from confluent_kafka.cimpl import KafkaError
from core.kafka_client_len import Consumer as SKConsumer, Producer as SKProducer, Admin as SKAdmin, Log as SKLog
from core.redis_client_len  import Consumer as SRConsumer, Producer as SRProducer
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