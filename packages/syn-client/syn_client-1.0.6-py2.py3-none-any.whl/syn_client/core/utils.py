#!/usr/bin/python3
# -*- coding: utf-8 -*-
from os import path, environ
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Set
import hashlib
from json import load
import sys
import linecache
import uuid
import socket
import platform


class Utils(object):

    
    def __init__(self):
        pass

    @staticmethod
    def basepath(*path_add):
        APP_PATH = path.dirname(path.dirname(path.abspath(__file__)))
        ROOT_PATH = path.dirname(APP_PATH)
        return path.join(APP_PATH, *path_add)

    @staticmethod
    def get_epoch(date_ini: str, date_end: str) -> Set:
        d1 = datetime.strptime(date_ini, "%Y-%m-%d")
        d2 = datetime.strptime(date_end, "%Y-%m-%d")
        delta = d2 - d1
        epoch = datetime.utcfromtimestamp(0)
        ret = set()
        for i in range(delta.days + 1):
            new_date = d1 + timedelta(days=i)
            res_epoch_ini = (new_date - epoch).total_seconds()
            res_epoch_end = (
                (new_date + timedelta(
                    hours=23, minutes=59, seconds=59)) - epoch).total_seconds()
            ret.add((res_epoch_ini, res_epoch_end))
        return ret

    @staticmethod
    def print_exception():
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        ret = {
            'type': "exception",
            'file_name': filename,
            'line': lineno,
            'expresion': line.strip(),
            'error': exc_obj
        }
        # return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(
        #     filename, lineno, line.strip(), exc_obj)
        return ret

    @staticmethod    
    def generate_hash(text):
        aux = hashlib.sha256()
        aux.update(text.encode('utf-8'))
        return aux.hexdigest()
        
    @staticmethod
    def get_enviroment() -> Dict:
        enviroments = load(open(Utils.basepath('config', 'enviroment.json')))
        sc_enviroment = environ.get('sc_enviroment', 'media')
        file_name = enviroments.get(sc_enviroment, 'media.ini')
        ret = {'file_name': file_name, 'sc_enviroment': sc_enviroment}
        return ret

    @staticmethod
    def md5sum(obj: str) -> str:
        try:
            md5lib = hashlib.md5()
            md5lib.update(obj.encode('utf-8'))
            return md5lib.hexdigest()
        except Exception as ex:
            print("md5sum Error: {}".format(ex))
            return '0'


class SysInfo(object):

    def __init__(self, *args, **kwargs):
        pass
    
    @staticmethod
    def ip() -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ret = s.getsockname()[0]
        s.close()
        return ret

    @staticmethod
    def host_name() -> str:
        ret = ''
        try:
            ret = platform.node()
        except Exception as e:
            print(e)
        finally:
            return ret
    
    @staticmethod
    def os_name() -> str:
        ret = ''
        try:
            ret = platform.system()
        except Exception as e:
            print(e)
        finally:
            return ret  

    @staticmethod
    def os_version() -> str:
        ret = ''
        try:
            ret = platform.release()
        except Exception as e:
            print(e)
        finally:
            return ret  

    @staticmethod
    def plataform_architecture() -> str:
        ret = ''
        try:
            ret = platform.machine()
        except Exception as e:
            print(e)
        finally:
            return ret

    @staticmethod
    def get_uuid() -> str:
        try:
            host_uuid = uuid.uuid1()
            ret = '-'.join(host_uuid.urn.split('-')[-3:])
        except Exception as ex:
            print("md5sum Error: {}".format(ex))
            ret = '0000'
        finally:
            return ret

    @staticmethod
    def client_version() -> str:
        return '1.0.0'