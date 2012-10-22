'''This module contains classes used by pool core to interact with the rest of the pool.
   Default implementation do almost nothing, you probably want to override these classes
   and customize references to interface instances in your launcher.
   (see launcher_demo.tac for an example).
''' 

import time
from twisted.internet import reactor, defer

import stratum.logger
log = stratum.logger.get_logger('interfaces')

from decimal import Decimal

from stratum import settings

import MySQLdb as db
import sqlalchemy.pool as pool

db = pool.manage(db)

class WorkerManagerInterface(object):
    def __init__(self):
        # Fire deferred when manager is ready
        self.on_load = defer.Deferred()
        self.on_load.callback(True)
        
    def authorize(self, worker_name, worker_password):
        return True

class ShareLimiterInterface(object):
    '''Implement difficulty adjustments here'''
    
    def submit(self, connection_ref, current_difficulty, timestamp):
        '''connection - weak reference to Protocol instance
           current_difficulty - difficulty of the connection
           timestamp - submission time of current share
           
           - raise SubmitException for stop processing this request
           - call mining.set_difficulty on connection to adjust the difficulty'''
        pass
    
class ShareManagerInterface(object):

    def __init__(self):
        # Fire deferred when manager is ready
        self.on_load = defer.Deferred()
        self.on_load.callback(True)

        self.share_count = 0
        self.last_rated = time.time()

    def on_network_block(self, prevhash):
        '''Prints when there's new block coming from the network (possibly new round)'''
        pass
    
    def on_submit_share(self, worker_name, block_header, block_hash, shares, timestamp, is_valid):
        #log.info("%s %s %s" % (block_hash, 'valid' if is_valid else 'INVALID', worker_name))
        self.share_count += 1
        now = time.time()
        elapsed = now - self.last_rated
        target = 1
        if hasattr(settings, 'POOL_TARGET'):
            target = settings.POOL_TARGET
        if elapsed > 60:
            rate = Decimal(((float(self.share_count) / elapsed) * 4294967296 * target) / 1000000000)
            self.last_rated = now
            self.share_count = 0
            if rate > 0:
                log.info("Hashrate: %.03f GH/s" % (rate))

        connection = None
        try:
            connection = db.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWORD, settings.MYSQL_DBNAME)
            cursor = connection.cursor()
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            if not cursor.execute('UPDATE workers SET last_update="%s" WHERE name="%s";' % (timestamp, worker_name)):
                cursor.execute('INSERT INTO workers (name, last_update) VALUES ("%s", "%s");' % (worker_name, timestamp))
            connection.commit()
        finally:
            if connection:
                connection.close()

    
    def on_submit_block(self, is_accepted, worker_name, block_header, block_hash, timestamp):
        log.info("Block %s %s" % (block_hash, 'ACCEPTED' if is_accepted else 'REJECTED'))
    
class TimestamperInterface(object):
    '''This is the only source for current time in the application.
    Override this for generating unix timestamp in different way.'''
    def time(self):
        return time.time()

class PredictableTimestamperInterface(TimestamperInterface):
    '''Predictable timestamper may be useful for unit testing.'''
    start_time = 1345678900 # Some day in year 2012
    delta = 0
    
    def time(self):
        self.delta += 1
        return self.start_time + self.delta
        
class Interfaces(object):
    worker_manager = None
    share_manager = None
    share_limiter = None
    timestamper = None
    template_registry = None
    
    @classmethod
    def set_worker_manager(cls, manager):
        cls.worker_manager = manager    
    
    @classmethod        
    def set_share_manager(cls, manager):
        cls.share_manager = manager

    @classmethod        
    def set_share_limiter(cls, limiter):
        cls.share_limiter = limiter
    
    @classmethod
    def set_timestamper(cls, manager):
        cls.timestamper = manager
        
    @classmethod
    def set_template_registry(cls, registry):
        cls.template_registry = registry