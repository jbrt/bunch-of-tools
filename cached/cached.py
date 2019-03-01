# coding: utf-8

import logging
import pickle
from functools import wraps, partial
from hashlib import md5
from inspect import getmodule

from redis import Redis
from redis.exceptions import TimeoutError, AuthenticationError, ConnectionError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s %(message)s')


def cached(func=None, redis_host: str = 'localhost', timeout: int = 60,
           redis_port=6379, redis_db=0, key_prefix: str = None):
    """
    Decorator function to add Redis caching capability to functions
    :param redis_host: (str) IP or hostname where Redis is installed
    :param func: (function) the decorated function
    :param timeout: (int) the Redis timeout/TTL (default: 60 secs)
    :param redis_port: (int) the Redis TCP port (default: 6379)
    :param redis_db: (int) the Redis DB to use (default: 0)
    :param key_prefix: (str) a prefix for the redis keys (optional)
    :return: reference to the decorator function
    """

    # This code allow this decorator to decorate himself
    if not func:
        return partial(cached,
                       timeout=timeout,
                       redis_host=redis_host,
                       key_prefix=key_prefix)

    # Will be used for the Redis key construction
    module_name = getmodule(func).__name__
    func_name = func.__name__

    _name = 'cached-decorator'
    logger.info(f'({_name}) Beginning work')

    @wraps(func)
    def decorated_function(service, *args, **kwargs):
        """
        The main decorator function
        :param service: 'service' == self because it's the first argument of each object method
        :param args: (list) list of arguments
        :param kwargs: (dict) keywords arguments
        :return: (list) data from the decorated function
        """
        # Built the Redis key that we'll use to store data later
        args_tuple = (list(args), dict(kwargs))
        args_key = md5(pickle.dumps(args_tuple)).hexdigest()
        redis_key = f'{key_prefix or ""}_cache_{module_name}.{func_name}.{args_key}'

        # Get the Redis client
        redis = Redis(host=redis_host, port=redis_port, db=redis_db)

        try:
            # If the key already exists in Redis, we use it to retrieve the
            # data
            if redis.exists(redis_key):
                logger.info(f'({_name}) Found an active key in Redis ({redis_key})')
                # If no_cache is set in function arguments, we invalidate the
                # cache and returns the data directly from the function
                if 'no_cache' in kwargs and kwargs['no_cache']:
                    logger.warning(f'({_name}) no_cache variable at True: bypassing cache')
                    redis.delete(redis_key)
                    response = func(service, *args, **kwargs)

                # Else, we can retrieve the data from Redis
                else:
                    response = pickle.loads(redis.get(redis_key))

            # If the key doesn't exists, execute the decorated function and
            # store the result in Redis
            else:
                logger.info(f'({_name}) No key found in Redis load data from function')
                response = func(service, *args, **kwargs)
                redis.set(redis_key, pickle.dumps(response), ex=timeout)

        except (TimeoutError, AuthenticationError, ConnectionError) as error:
            logger.warning(f'({_name}) Something goes wrong with Redis')
            logger.warning(f'({_name}) Can\'t cache data (cause: {error})')
            logger.warning(f'({_name}) Retrieve data from function directly')
            return func(service, *args, **kwargs)
        else:
            logger.info(f'({_name}) End of decorator. Returns data')
            return response

    return decorated_function
