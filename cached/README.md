# Cached decorator

Cached is a small decorator based on Redis for caching responses of the 
decorated function. This decorator used a Lazy Loading algorithm.

## Usage 

This decorator use these arguments:

````python
def cached(func=None, redis_host: str = 'localhost', timeout: int = 60,
           redis_port=6379, redis_db=0, key_prefix: str = None):
````

- redis_host: IP or hostname where Redis is installed
- timeout: the number of seconds where the data lives into Redis before expiring
- redis_port: the TCP port where Redis listen
- redis_db: the Redis database number to use
- key_prefix: a string that can be used as Redis key prefix

## Dependencies

This tool used only Redis as dependency.

## Algorithm

TBD

## Example

Code sample:

```python
from cached.cached import cached


@cached(redis_host='localhost')
def display_hello(name: str):
    print(f'Hello {name} !')


if __name__ == '__main__':
    display_hello('John')
```

Console output when launched after the first launch:

````sh
2019-02-27 17:19:46,475 INFO (cached-decorator) Beginning work
2019-02-27 17:19:46,476 INFO (cached-decorator) Beginning work
2019-02-27 17:19:46,485 INFO (cached-decorator) No key found in Redis load data from function
2019-02-27 17:19:46,486 INFO (cached-decorator) End of decorator. Returns data
Hello John !
````

Console output when launched after the second launch (just few seconds after):

````sh
2019-02-27 17:20:12,590 INFO (cached-decorator) Beginning work
2019-02-27 17:20:12,590 INFO (cached-decorator) Beginning work
2019-02-27 17:20:12,599 INFO (cached-decorator) Found an active key in Redis (_cache___main__.display_hello.21b48b22581ff3caca703be2cfbf05e0)
2019-02-27 17:20:12,600 INFO (cached-decorator) End of decorator. Returns data
````

As you can see, the data has been retrieved from Redis.

## License

This tool is under MIT license.