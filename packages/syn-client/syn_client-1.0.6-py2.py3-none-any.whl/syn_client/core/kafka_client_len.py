#!/usr/bin/python3
# -*- coding: utf-8 -*-
from confluent_kafka import Consumer as KConsumer
from confluent_kafka import Producer as KProducer
from confluent_kafka.admin import AdminClient
from confluent_kafka.admin import NewTopic
from confluent_kafka.admin import NewPartitions
from confluent_kafka.cimpl import KafkaError
from confluent_kafka import TopicPartition
from typing import List, Dict, Tuple, Set, TypeVar
from syn_client.core.utils import Utils
from datetime import datetime
from json import loads, dumps
from typing import List
import random
import uuid


class Consumer(object):
    is_connected = False
    def __init__(self,
            server: str,
            session_timeout_ms: int = 0,
            group: str = uuid.uuid1()):
        """
        
        Arguments:
            server {str} -- host ip or name address
        
        Keyword Arguments:
            session_timeout_ms {int} -- ms to desconnect idle (default: {0})
            group {str} -- group to use in connection (default: {uuid.uuid1()})
        """
        self._conf = {
            'bootstrap.servers': server,
            'group.id': group,
            'enable.auto.commit': True,
            'stats_cb': Consumer.on_stats,
            'error_cb': Consumer.on_error,
            'on_commit': Consumer.on_commit,
            'default.topic.config': {
                'auto.offset.reset': 'smallest',
                # 'compression.codec': 'snappy' # add compress option, valid option [(gzip, snappy, lz4)
            }
        }
        if session_timeout_ms > 0:
            self._conf['session.timeout.ms'] = session_timeout_ms
        self._consumer = None
        self.msg_consumed_count = 0
        self.msg = None
        self.num_partitions = 1
        self._consumer = None
        self.topics = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.close_connection()
        except Exception as e:
            print("close connection in EXIT, err: {}".format(e))

    def __del__(self):
        pass

    @staticmethod    
    def on_error(error: KafkaError): 
        print('KafkaError: %s', error.str())

    @staticmethod
    def on_commit(error: KafkaError, partitions):
        if error:
            print('On commit error: {}'.format(error.str()))
        else:
            print('Commited')

    @staticmethod
    def on_stats(stats_json_str):
        stats_json = loads(stats_json_str)
        print('\nKAFKA Stats: {}\n'.format(stats_json))

    @staticmethod
    def on_assignment(consumer, partitions):
        pass

    def connect(self, topics: List):
        """Connect to kafka topic
        
        Arguments:
            topics {List} -- name of topic to use
        """
        self.topics = topics
        self._consumer = KConsumer(**self._conf)
        self._consumer.subscribe(topics, on_assign=Consumer.on_assignment)
        Consumer.is_connected = True

    def close_connection(self):
        """Close the current connection
        """
        if self._consumer is not None:
            self._consumer.close()
            self.is_connected = False

    def get_message(self, timeout: float = 0) -> Dict:
        """[summary]
        
        Keyword Arguments:
            timeout {float} -- ms to use in send (default: {0})
        
        Returns:
            Dict -- return message obtained
        """
        result = None
        try:
            if timeout == 0:
                self.msg = self._consumer.poll()
            else:
                self.msg = self._consumer.poll(timeout=timeout)
            if self.msg:
                self.msg_consumed_count += 1
                result = {
                    'error': None,
                    'msg': None,       
                    'information': {
                       'topic': self.msg.topic(),
                        'partition': self.msg.partition(),
                        'offset': self.msg.offset(),
                    }
                }
                if self.msg.error():
                    result['error'] = {
                        'error_name': self.msg.error().name(),
                        'error_code': self.msg.error().code(),
                        'error_msg': self.msg.error().str()
                    }
                else:
                    result['msg'] = loads(self.msg.value().decode('utf-8'))
        except Exception as e:
            print(e)
        return result


class Producer(object):
    is_deliveried = False
    msg_offset = -1001
    partition = -1
    is_connected = False
    def __init__(self,
            server: str,
            session_timeout_ms: int = 6000,):
        """
        
        Arguments:
            server {str} -- host ip or name address
        
        Keyword Arguments:
            session_timeout_ms {int} -- time out from disconnect client (default: {6000})

        """
        self._conf = {
            'bootstrap.servers': server,
        }
        if session_timeout_ms > 0:
            self._conf['session.timeout.ms'] = session_timeout_ms
        self._producer = KProducer(**self._conf)
        Producer.is_deliveried = False
        Producer.patition = -1
        self.topic = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.close_connection()
        except Exception as e:
            print("close connection in EXIT, err: {}".format(e))

    def __del__(self):
        pass

    @staticmethod
    def on_delivery_callback(err, msg):
        if err:
            print('Message failed delivery: {}'.format(err))
        else:
            Producer.is_deliveried = True
            Producer.msg_offset = msg.offset()
            Producer.partition = msg.partition()
            print('Message delivered to {} part: {} offset: {}'.format(
                msg.topic(), msg.partition(), msg.offset()))

    def connect(self, topic: str):
        """Connect to kafka topic
        
        Arguments:
            topics {str} -- name of topic to use
        """
        self.topic = topic
        Producer.is_connected = True
 
    def close_connection(self):
        """Close the current connection
        """
        if self._producer is not None:
            Producer.is_connected = False
    
    def send_message(self, msg: Dict) -> bool:
        """Send message to topic
        
        Arguments:
            msg {str} -- message to send
        
        Returns:
            bool -- true if send it, otherwise false
        """
        ret = False
        try:
            Producer.is_deliveried = False
            self._producer.produce(
                self.topic, dumps(msg), callback=self.on_delivery_callback)
            # self._producer.poll(0)
            self._producer.flush()
            ret = True
        except Exception:
            pass
        return ret


class Admin(object):
    def __init__(self,
            server: str,
            session_timeout_ms: int = 6000,):
        """
        
        Arguments:
            server {str} -- host ip or name address
        
        Keyword Arguments:
            session_timeout_ms {int} -- time out from disconnect client (default: {6000})

        """
        self._conf = {
            'bootstrap.servers': server,
        }
        if session_timeout_ms > 0:
            self._conf['session.timeout.ms'] = session_timeout_ms

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __del__(self):
        pass

    def expand_partitions(self, topic: str, num_partitions: int = 1) -> bool:
        """Expand num of partiton, the number have be upper to ciurrent num of partitions
        
        Arguments:
            topic {str} -- name of the topic
        
        Keyword Arguments:
            num_partitions {int} -- [num of partition to increment] (default: {1})
        
        Returns:
            bool -- true if expand it, otherwise false
        """
        partitons = NewPartitions(topic, num_partitions)
        ac = AdminClient(self._conf)
        ret = ac.create_partitions([partitons])
        if ret[topic].result():
            return False
        else:
            return True

    def create_topic(self,
            topic: str,
            num_partitions: int = 1,
            retention_ms: int = 604800000,
            delete_retention_ms: int = 30000) -> bool:
        """Create the topic to use
        
        Arguments:
            topic {str} -- name of the topic
        
        Keyword Arguments:
            num_partitions {int} -- num of partition to create (default: {1})
        
        Returns:
            bool -- true if create it, otherwise false
        """
        config={
            'retention.ms': retention_ms,
            'delete.retention.ms': delete_retention_ms}
        ntopic = NewTopic(topic, num_partitions, 1, config=config)
        ac = AdminClient(self._conf)
        ret = ac.create_topics([ntopic])
        if ret[topic].result():
            return False
        else:
            return True

    def remove_topic(self, topic: str) -> bool:
        """Remove a topic
        
        Arguments:
            topic {str} -- name of the topic
        
        Returns:
            bool -- true if remove it, otherwise false
        """
        ac = AdminClient(self._conf)
        ret = ac.delete_topics([topic])
        if ret[topic].result():
            return False
        else:
            return True


class Log(object):

    def __init__(self, server):
        self._config = {
            'server': server
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __del__(self):
        pass

    def create_log(self, msg, status) -> Dict:
        return {
            'msg': msg,
            'id': Utils.generate_hash(dumps(msg)),
            'status': status,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def _msg(self, msg: str, log_type: str) -> bool:
        ret = False
        try:
            with Producer(**self._config) as p:
                p.connect(topic='queue_log')
                p.send_message(self.create_log(msg=msg, status=log_type))
            return True
        except Exception:
            pass
        return ret

    def msg_created(self, msg):
        self._msg(msg=msg, log_type='created')

    def msg_in_process(self, msg):
        self._msg(msg=msg, log_type='in_process')

    def msg_done(self, msg):
        self._msg(msg=msg, log_type='done')

    def msg_error(self, msg):
        self._msg(msg=msg, log_type='error')