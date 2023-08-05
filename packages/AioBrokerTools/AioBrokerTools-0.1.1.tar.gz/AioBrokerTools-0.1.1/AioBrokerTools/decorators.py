import functools
import inspect

import aiojobs


def rpc_method(broker, name=None):
    def rpc_method_decorator(func, name=name):
        if name is None:
            name = func.__name__
            # name = '_'.join(func.__qualname__.split('.')[2:])
        broker.add_rpc_func(name, func)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return  wrapper
    return rpc_method_decorator


def event(broker, exchange, routing_key):
    def event_decorator(func, exchange=exchange, routing_key=routing_key):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            event_context = dict()
            
            argnames, _, _, defaults = inspect.getargspec(func) 
            
            if defaults:
                event_context.update(dict(zip(reversed(argnames), reversed(defaults))))
            if args:
                event_context.update(dict(zip(argnames, args)))
            event_context.update(kwargs)
            if 'self' in event_context:
                del event_context['self']
            if 'event_context' in argnames:
                del event_context['event_context']
                kwargs['event_context'] = event_context
            result = await func(*args, **kwargs)
            
            await broker.scheduler.spawn(broker.publish_event(exchange, routing_key, event_context))
            
            return result
        return  wrapper
    return event_decorator