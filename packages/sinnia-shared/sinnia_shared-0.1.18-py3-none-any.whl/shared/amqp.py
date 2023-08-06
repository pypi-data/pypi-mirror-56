import pika, logging, time, threading, urllib2, json

# from warnings import simplefilter
# simplefilter("ignore", "user")


## Configurable parameters

_loglevel = logging.INFO
_publish_sleeptime = 60
_default_helper_conf = "big"
_default_amqp_conf = "db"

# onde: ec2-54-208-87-165.compute-1.amazonaws.com:15672
_helper_conf = { 
    "big": {
        'helper_sleeptime' : 300, # in seconds
        'ram_limit' : 25, # value in GB
        'host' : 'localhost',
        'user' : 'trb',
        'pass' : "clm28'Anglos",
        'virtual_host' :'twttr'        
    },
    "small": {
        'helper_sleeptime' : 300, # in seconds
        'ram_limit' : 3,# value in GB
        'host' : 'localhost',
        'user' : 'trb',
        'pass' : "clm28'Anglos",
        'virtual_host' :'twttr'        
    },
    "local": {
        'helper_sleeptime' : 300, # in seconds
        'ram_limit' : 1, # value in GB
        'host' : 'localhost',
        'user' : 'trb',
        'pass' : "clm28'Anglos",
        'virtual_host' :'twttr'
    }
}

_amqp_conf = {
    "db": {
        'host' : 'localhost',
        #'host' : 'stream-rabbit-2-0.sinniaws.com', # rabbit-2-0
        #'host' : '107.21.235.136', # capture
        'user' : 'trb',
        'pass' : "clm28'Anglos",
        'virtual_host' :'twttr',
        'exchange' : 'capture',
        'routing_key' :'rest.%s.no-log'
    },
    "file": {
        'host' : 'localhost',
        'user' : 'trb',
        'pass' : "clm28'Anglos",
        'virtual_host' :'twttr',
        'exchange' : 'capture_to_file',
        'routing_key' :'rest.%s.no-log'
    }
}

## Logger init
    
_instances = {}

## Class definition
class AMQPUtil():
    logging.basicConfig(level=logging.DEBUG)

    def __init__(self, with_helper=False):
        self.do_slow_down = False
        self.ram_current = None
        
        conf = _helper_conf.get(_default_helper_conf, _helper_conf['local'])
        self.helper = AMQPHelper(conf['helper_sleeptime'], conf['host'], 
                                 conf['user'], conf['pass'], conf['ram_limit'])
        if with_helper:
            self.helper.start()
        conf = _amqp_conf.get(_default_amqp_conf, _amqp_conf['db'])
        self._parameters = pika.ConnectionParameters(
            credentials=pika.PlainCredentials(conf['user'], conf['pass']),
            host=conf['host'], virtual_host=conf['virtual_host'])
        self._connection = None
        self._channel = None
        logging.info("Instance of AMQPUtil initialized")
        logging.info("Credentials: %s, %s, %s" % (conf['host'], conf['user'], 
                                                  conf['pass']))


    def _getChannel(self):
        global _publish_sleeptime
        if self._connection is None or self._channel is None \
                or self._connection.is_closed or self._channel.is_closed \
                or not self._connection.is_open:
            logging.info('Reconnecting ...')
            self._connection = pika.BlockingConnection(self._parameters)
            def _handleBackpressure():
                self.helper.tcp_handler()
            self._channel = self._connection.channel()
        if self.helper.do_slow_down():
            logging.warn('Sleeping ...')
            time.sleep(_publish_sleeptime)
            logging.warn('Awake ...')
        return self._channel

    @staticmethod
    def _getInstance(config_name = None):
        global _instances
        if not config_name: config_name = _default_amqp_conf
        instance = _instances.get(config_name)
        if not instance:
            instance = AMQPUtil()
            _instances[config_name] = instance
        return instance
        
    @staticmethod
    def publish(client, message, config = None, retry=0):
        try:
            if not client : client = "sinnia-new"
            client_key = (lambda c, m: m.get(c) if m.get(c) else c)\
                         (client, { "all": "all", 
                                    "sinnia": "sinnia", 
                                    "sinnia-new": "sinnia-new" })
            conf = _amqp_conf.get(config, _amqp_conf[_default_amqp_conf])
            routing_key=conf['routing_key'] % str(client_key)
            AMQPUtil._getInstance(config)\
                    ._getChannel().basic_publish(exchange=conf['exchange'],
                                                 routing_key=routing_key,
                                                 body=message)
            #logging.debug("Message publish virtual_host: %s, "
            #              "exchange: %s, routing_key: %s, body: %s"
            #              % (conf['virtual_host'], conf['exchange'], 
            #                 routing_key, message))
        except:
            retry += 1
            logging.info("Retry .... %s" % retry)
            AMQPUtil.publish(client, message, config, retry)

class AMQPHelper(threading.Thread):

    def __init__(self, sleeptime, host, user, passwd, ram_limit):
        self.api_url = 'http://%s:15672/api/nodes' % host 
        self.ram_limit = ram_limit * 1000000000
        self.sleeptime = sleeptime
        self.current_ram = 0
        self.tcp_trigered = False
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, self.api_url, user, passwd)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        threading.Thread.__init__(self)

    def get_ram(self):
        return self.current_ram

    def is_ram_exceded(self):
        return self.ram_limit < self.get_ram()

    def is_tcp_trigered(self):
        if self.tcp_trigered:
            self.tcp_trigered = False
            return True
        return False

    def tcp_handler(self):
        self.tcp_trigered = True

    def do_slow_down(self):
        return self.is_ram_exceded() or self.is_tcp_trigered()
        
    def run(self):
        while 1:
            try:
                response = urllib2.urlopen(self.api_url)
                data = json.loads(response.read())
                max_ram = 0
                for node in data:
                    ram = node.get('mem_used', 0)
                    if max_ram < ram: max_ram = ram
                self.current_ram = int(max_ram)
                logging.info("RAM: %sG" % (self.current_ram / 1000000000.0))
            except Exception as exc:
                logging.info("Could not obtain ram: %s" % self.api_url)
                logging.exception(exc)
            time.sleep(self.sleeptime)

