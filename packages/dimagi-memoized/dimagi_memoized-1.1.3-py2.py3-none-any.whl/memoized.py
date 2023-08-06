# See http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
from __future__ import absolute_import
from __future__ import print_function
import functools
from inspect import getcallargs, isfunction
try:
    from inspect import getfullargspec
except ImportError:
    # Fall back to getargspec, deprecated since Python 3.0
    from inspect import getargspec as getfullargspec


def memoized(fn):
    def _memoized(*args, **kwargs):
        cache, key = m.get_cache_and_key(args, kwargs)
        try:
            return cache[key]
        except KeyError:
            pass
        cache[key] = value = fn(*args, **kwargs)
        return value

    m = Memoized(fn)
    _memoized = functools.wraps(fn)(_memoized)
    _memoized.get_cache = m.get_cache
    _memoized.reset_cache = m.reset_cache
    return _memoized


def memoized_property(fn):
    return property(memoized(fn))


class Memoized(object):
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    >>> from memoized import memoized
    >>> @memoized
    ... def f(n=0):
    ...     return n**2
    >>> f()
    0
    >>> f.get_cache()
    {(0,): 0}
    >>> f(0)
    0
    >>> f.get_cache()
    {(0,): 0}
    >>> f(2)
    4
    >>> f(n=4)
    16
    >>> sorted(f.get_cache().items())
    [((0,), 0), ((2,), 4), ((4,), 16)]
    >>> @memoized
    ... class Person(object):
    ...     def __init__(self, first_name, last_name):
    ...         self.first_name = first_name
    ...         self.last_name = last_name
    ...     @memoized_property
    ...     def full_name(self):
    ...         print("Computing full name")
    ...         return "%s %s" % (self.first_name, self.last_name)
    ...     @memoized
    ...     def get_full_name(self):
    ...         print("Computing full name")
    ...         return "%s %s" % (self.first_name, self.last_name)
    ...     def __repr__(self):
    ...         return "%s(%r, %r)" % (self.__class__.__name__, self.first_name, self.last_name)
    ...     @memoized
    ...     def complicated_method(self, a, b=10, *args, **kwargs):
    ...         print("Calling complicated method")
    ...         return a, b, args, kwargs
    >>> p = Person("Danny", "Roberts")
    >>> p.get_full_name()
    Computing full name
    'Danny Roberts'
    >>> p.get_full_name()
    'Danny Roberts'
    >>> p.full_name
    Computing full name
    'Danny Roberts'
    >>> Person("Danny", "Roberts")._full_name_cache
    {(): 'Danny Roberts'}
    >>> p.full_name
    'Danny Roberts'
    >>> Person.get_full_name.get_cache(p)
    {(): 'Danny Roberts'}
    >>> p.complicated_method(5)
    Calling complicated method
    (5, 10, (), {})
    >>> p.complicated_method(5)
    (5, 10, (), {})
    >>> p.complicated_method(1, 2, 3, 4, 5, foo='bar')
    Calling complicated method
    (1, 2, (3, 4, 5), {'foo': 'bar'})
    >>> q = Person("Joe", "Schmoe")
    >>> q.get_full_name()
    Computing full name
    'Joe Schmoe'
    """
    def __init__(self, func):

        if isfunction(func):
            self.func = func
        else:
            def wrapped(*args, **kwargs):
                return func(*args, **kwargs)
            self.func = wrapped
        self.argspec = getfullargspec(self.func)
        if self.argspec.args and self.argspec.args[0] == u'self':
            self.is_method = True
            self.arg_names = self.argspec.args[1:]
        else:
            self.is_method = False
            self.arg_names = self.argspec.args
            self._cache = {}

    def get_cache(self, obj=None):
        if self.is_method:
            cache_attr = u'_%s_cache' % self.func.__name__
            try:
                cache = getattr(obj, cache_attr)
            except (KeyError, AttributeError):
                cache = {}
                setattr(obj, cache_attr, cache)
            return cache
        else:
            return self._cache

    def reset_cache(self, obj=None):
        self.get_cache(obj).clear()

    def get_cache_and_key(self, args, kwargs):
        obj = args[0] if self.is_method else None
        cache = self.get_cache(obj)
        key = self.get_key(args, kwargs)
        return cache, key

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def get_key(self, args, kwargs):
        """Get cache key from call arguments"""
        if not kwargs and not self.argspec.defaults:
            return args[1:] if self.is_method else args
        kwargs_name = self.argspec[2]  # FullArgSpec.varkw or ArgSpec.keywords
        values = getcallargs(self.func, *args, **kwargs)
        in_order = [values[arg_name] for arg_name in self.arg_names]
        if self.argspec.varargs:
            in_order.append(values[self.argspec.varargs])
        if kwargs_name:
            in_order.append(tuple(sorted(values[kwargs_name].items())))
        return tuple(in_order)
