#!/usr/bin/python3
# -*- coding: utf-8 -*-
from redis import Redis, ConnectionPool
from json import dumps, loads
from typing import List, Dict, Tuple, Set
from hashlib import sha256
from syn_client.core.utils import Utils
from datetime import datetime


class Consumer:

    def __init__(self, host: str, port: int, password: str = None, db: int = 0):
        """
        
        Arguments:
            host {str} -- host address
            port {int} -- host port
        
        Keyword Arguments:
            password {str} -- password to connect (default: {None})
            db {int} -- number of db to connect (default: {0})
        """
        self._topic = None
        self._config = {
            'host': host,
            'port': port,
            'db': db
        }
        if password:
            sha_pass = sha256(password.encode('utf8')).hexdigest()
            self._config['password'] = sha_pass
        self._conn_pool = None
        self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.close_connection()
        except Exception as e:
            print("close connection in EXIT, err: {}".format(e))

    def __del__(self):
        pass

    def connect(self, topic: str):
        """Connect to redis server
        
        Arguments:
            topic {str} -- topic or collection no use
        """
        self._topic = topic
        self._conn_pool = ConnectionPool(**self._config)
        self._conn = Redis(connection_pool=self._conn_pool)

    def close_connection(self):
        """Close the current connection
        """
        if self._conn_pool:
            self._conn_pool.disconnect()
            self._conn = None
            self._conn_pool = None

    def get_message(self) -> Dict:
        """Read a message in json format
        
        Returns:
            Dict -- return message obtained
        """
        try:
            row = self._conn.lpop(self._topic)
            return {
                'msg': loads(row),
                'error': None,                
                'information': {
                    'topic': self._topic,
                    'partition': 0,
                    'offset': -1,
                }
            }
        except Exception:
            return None


class Producer:

    def __init__(self, host: str, port: int, password: str = None, db: int = 0):
        """
        
        Arguments:
            host {str} -- host address
            port {int} -- host port
        
        Keyword Arguments:
            password {str} -- password to connect (default: {None})
            db {int} -- number of db to connect (default: {0})
        """
        self._topic = None
        self._config = {
            'host': host,
            'port': port,
            'db': db
        }
        if password:
            sha_pass = sha256(password.encode('utf8')).hexdigest()
            self._config['password'] = sha_pass
        self._conn_pool = None
        self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.close_connection()
        except Exception as e:
            print("close connection in EXIT, err: {}".format(e))

    def __del__(self):
        pass

    def connect(self, topic: str):
        """Connect to redis server
        
        Arguments:
            topic {str} -- topic or collection no use
        """
        self._topic = topic
        self._conn_pool = ConnectionPool(**self._config)
        self._conn = Redis(connection_pool=self._conn_pool)

    def close_connection(self):
        """Close the current connection
        """
        if self._conn_pool:
            self._conn_pool.disconnect()
            self._conn = None
            self._conn_pool = None

    def send_message(self, msg: Dict) -> bool:
        """Send a message in json format
        
        Arguments:
            msg {dict} -- message to send in json format
        
        Returns:
            bool -- true if can send message else false
        """
        self._conn.rpush(self._topic, dumps(msg))
        return True


class Log(object):

    def __init__(self, host: str, port: int, password: str = None, db: int = 0):
        self._config = {
            'host': host,
            'port': port,
            'db': db
        }
        if password:
            self._config['password'] = password

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __del__(self):
        pass

    def _create_log(self, msg, status) -> Dict:
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
                p.send_message(self._create_log(msg=msg, status=log_type))
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