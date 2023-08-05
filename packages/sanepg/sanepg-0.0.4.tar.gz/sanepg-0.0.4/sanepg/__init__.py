
from .pool import Pool

import tornado.ioloop

# a generic error class for throwing exceptions
class SaneError(Exception):
    def __init__(self, fmt, *args):
        self.message = fmt % args

    def __str__(self):
        return self.message


# factory function to connect a pool
def connect(dsn, *args, **kwds):
    pool = Pool(dsn, *args, **kwds)
    ioloop = tornado.ioloop.IOLoop.current()
    try:
        return ioloop.run_sync(pool.connect)
    except sanepg.SaneError as e:
        raise
