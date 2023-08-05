### Version 0.1
import sys, os, logging, yaml 
from datetime import time, timedelta, datetime, tzinfo, date

import pymysql

class Utils(object):
    
    #default_frmttr = '%(levelname)-5s - %(asctime)-15s %(message)s'    
    default_frmttr = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    default_root_frmttr = '%(asctime)s - %(levelname)s - %(message)s'    
    default_level = 'DEBUG'
    
    conf = dict()

    active_connections = dict()

    def init(self, conf_file_path, trace_enabled= False, log_name_param= None):
        self.trace_enabled = trace_enabled
        with open(conf_file_path) as conf_file:
            self.conf = yaml.load(conf_file, Loader=yaml.FullLoader)

        log_name = self.conf.get("log_name", log_name_param)
        log_file = self.conf.get("log_file", "logs/default.log")
        log_to_console = self.conf.get("log_to_console")
        logger = logging.getLogger(log_name)
            
        print('config log_name: %s' % log_name)
        print('config log_file: %s' % log_file)
        print('config log_to_console: %s' % log_to_console)
        # Always log to Console
        # Log to File unless log_file = 'None'
        # Console logger has default level and formatting
        # File logger can be configured with 'log_level' and 'log_formatter'
        self.init_console_logger(log_name)
        if log_file == "None":
            return
        self.init_file_logger(log_file, log_name)
        

    def set_log_name(self, name):
        if name != None:
            return name
        return self.conf.get("log_name", __name__)
        
    def init_console_logger(self, logger_name = 'root'):
        level = logging.DEBUG
        frmt = self.default_root_frmttr
        frmttr = logging.Formatter(frmt)
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)

        sh = logging.StreamHandler()
        sh.setFormatter(frmttr)
        sh.setLevel(level)
        logger.addHandler(sh)
        logger.debug("init_console_logger configured: {}".format(logger_name))
        
    def init_file_logger(self, log_file, logger_name='default'):
        d = os.path.dirname(log_file)
        if not os.path.exists(d):
            os.makedirs(d)

        level = self.conf.get("log_level", self.default_level)
        frmt = self.conf.get("log_formatter", self.default_frmttr)
        frmttr = logging.Formatter(frmt)
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        fh = logging.FileHandler(log_file, mode='a', encoding='utf8')
        fh.setFormatter(frmttr)
        fh.setLevel(level)
        logger.addHandler(fh)
        logger.debug("init_file_logger configured: {}".format(logger_name))

    def from_config(self, path):
        try:
            path_args = path.split('.')
            current = self.conf
            for arg in path_args:
                current = current.get(arg)
            return current
        except Exception as ex:
            logging.error("Error extracting from config for path '%s'", path)
            raise ex

    def get_conn(self, name, register_conn=True):
        if not register_conn:
            return self._open_conn(name)
        conn = self.active_connections.get(name)
        if not conn:
            #db_config = conf.get('db_config').get(name)
            conn = self._open_conn(name)
            if conn:
                self.active_connections[name] = conn
        return conn
    
    def _open_conn(self, name):
        db_config = self.from_config('db_config.' + name)
        if db_config:
            return pymysql.connect(
                host = db_config.get("host"),
                user = db_config.get("user"),
                password = db_config.get("passwd"),
                db = db_config.get("db"),
                charset = db_config.get("charset"),
                use_unicode = False)
        else:
            sys.exit("DB config not found for name '%s'" % name)
        return None
    
    def close_conn(self, name):
        conn = self.active_connections.get(name)
        if conn:
            conn.close()
            self.active_connections.remove(name) # .pop ??
        
    def get_active_connections(self):
        return self.active_connections.values()

    def close_active_connections(self):
        for conn in self.active_connections.itervalues(): 
            conn.close()
        self.active_connections.clear()                                

    @staticmethod
    def daterange(start_date, end_date):
        n = -1
        for n in range(int ((end_date - start_date).days) - 1):
            ref_date = start_date + timedelta(n)
            yield (ref_date, ref_date + timedelta(1))
        if n == -1 :
            yield (start_date, end_date)
        else: 
            yield (start_date + timedelta(n + 1), end_date)

    @staticmethod
    def csv_mapper(row):
        return map(lambda val: val if val is not None else "NULL", row)

    @staticmethod
    def insert_mapper(row, default = "NULL", conn = None):
        def mapper(val):
            if val is not None:
                if isinstance(val, (int, long)):
                    return str(val)
                else:
                    if conn:
                        return "'%s'" % (conn.escape_string(str(val)))
                    else:
                        return "'%s'" % (str(val))
                                     #.replace('\\', "").replace("'", "\\'"))
            return default
        return map(mapper, row)

    # @staticmethod
    # def insert_mapper(row):
    #     for val in row:
    #         yield str(val) if isinstance(val, (int, long)) \
    #             else "'%s'" % str(val).replace("'", "\\'")

    def has_trace_enabled(self):
        return self.trace_enabled

    def response_as_json(self, r):
        if r.status_code == 400 or r.status_code != 200:
            logging.error('Error: %s' % str(r))
            return False
        if not r.encoding:
            r.encoding = 'utf-8'
        if self.has_trace_enabled():
            logging.debug('Json: %s...' % r.text[:500])
        return r.json()
