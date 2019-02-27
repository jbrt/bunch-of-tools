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

## Algorithm

TBD

## Example

```python
from cached.cached import cached


@cached(redis_host='localhost')
def display_hello(name: str):
    print(f'Hello {name} !')


if __name__ == '__main__':
    display_hello('John')
```

## License

This tool is under MIT license.