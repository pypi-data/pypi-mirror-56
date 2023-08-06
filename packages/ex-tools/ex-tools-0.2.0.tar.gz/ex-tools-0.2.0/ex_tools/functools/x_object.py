from functools import partial
from typing import Union, Dict, Iterable, Any, Callable


class XAbstract:
    @staticmethod
    def process_x(value, x):
        if isinstance(value, XAbstract):
            return type(value).__run__(value, x)
        else:
            return value

    def __wrap__(self, name, operation, repr_, *args, **kwargs):
        raise NotImplemented

    def __run__(self, x):
        return x

    # function call
    def __call__(self, *args, **kwargs):
        represent = \
            '{}({}, {})'.format(
                repr(self),
                ', '.join(map(repr, args)),
                ', '.join(map(lambda kv: kv[0] + '=' + repr(kv[1]), kwargs.items()))
            ) if args and kwargs else \
            '{}({})'.format(
                repr(self),
                ', '.join(map(repr, args)),
            ) if args else \
            '{}({})'.format(
                repr(self),
                ', '.join(map(lambda kv: kv[0] + '=' + repr(kv[1]), kwargs.items()))
            ) if args else \
            '{}()'.format(repr(self))
        return self.__wrap__('__call__', False, represent, *args, **kwargs)

    # comparision
    def __eq__(self, other):
        return self.__wrap__('__eq__', True, '{} == {}'.format(*map(repr, (self, other))), other)

    def __ne__(self, other):
        return self.__wrap__('__ne__', True, '{} != {}'.format(*map(repr, (self, other))), other)

    def __gt__(self, other):
        return self.__wrap__('__gt__', True, '{} > {}'.format(*map(repr, (self, other))), other)

    def __lt__(self, other):
        return self.__wrap__('__lt__', True, '{} < {}'.format(*map(repr, (self, other))), other)

    def __le__(self, other):
        return self.__wrap__('__le__', True, '{} <= {}'.format(*map(repr, (self, other))), other)

    def __ge__(self, other):
        return self.__wrap__('__le__', True, '{} >= {}'.format(*map(repr, (self, other))), other)

    # operation
    def __add__(self, other):
        return self.__wrap__('__add__', True, '{}+{}'.format(*map(repr, (self, other))), other)

    def __sub__(self, other):
        return self.__wrap__('__sub__', True, '{}-{}'.format(*map(repr, (self, other))), other)

    def __mul__(self, other):
        return self.__wrap__('__mul__', True, '{}*{}'.format(*map(repr, (self, other))), other)

    def __pow__(self, other):
        return self.__wrap__('__pow__', True, '{}**{}'.format(*map(repr, (self, other))), other)

    def __matmul__(self, other):
        return self.__wrap__('__matmul__', True, '{}@{}'.format(*map(repr, (self, other))), other)

    def __truediv__(self, other):
        return self.__wrap__('__truediv__', True, '{}/{}'.format(*map(repr, (self, other))), other)

    def __floordiv__(self, other):
        return self.__wrap__('__floordiv__', True, '{}//{}'.format(*map(repr, (self, other))), other)

    def __mod__(self, other):
        return self.__wrap__('__mod__', True, '{}%{}'.format(*map(repr, (self, other))), other)

    # binary operation
    def __and__(self, other):
        return self.__wrap__('__and__', True, '{}&{}'.format(*map(repr, (self, other))), other)

    def __or__(self, other):
        return self.__wrap__('__or__', True, '{}|{}'.format(*map(repr, (self, other))), other)

    def __xor__(self, other):
        return self.__wrap__('__xor__', True, '{}^{}'.format(*map(repr, (self, other))), other)

    def __lshift__(self, other):
        return self.__wrap__('__lshift__', True, '{} << {}'.format(*map(repr, (self, other))), other)

    def __rshift__(self, other):
        return self.__wrap__('__rshift__', True, '{} >> {}'.format(*map(repr, (self, other))), other)

    # operation right
    def __radd__(self, other):
        return self.__wrap__('__radd__', True, '{}+{}'.format(*map(repr, (other, self))), other)

    def __rsub__(self, other):
        return self.__wrap__('__rsub__', True, '{}-{}'.format(*map(repr, (other, self))), other)

    def __rmul__(self, other):
        return self.__wrap__('__rmul__', True, '{}*{}'.format(*map(repr, (other, self))), other)

    def __rpow__(self, other):
        return self.__wrap__('__rpow__', True, '{}**{}'.format(*map(repr, (other, self))), other)

    def __rmatmul__(self, other):
        return self.__wrap__('__rmatmul__', True, '{}@{}'.format(*map(repr, (other, self))), other)

    def __rtruediv__(self, other):
        return self.__wrap__('__rtruediv__', True, '{}/{}'.format(*map(repr, (other, self))), other)

    def __rfloordiv__(self, other):
        return self.__wrap__('__rfloordiv__', True, '{}//{}'.format(*map(repr, (other, self))), other)

    def __rmod__(self, other):
        return self.__wrap__('__rmod__', True, '{}%{}'.format(*map(repr, (other, self))), other)

    # binary operation right
    def __rand__(self, other):
        return self.__wrap__('__rand__', True, '{}&{}'.format(*map(repr, (other, self))), other)

    def __ror__(self, other):
        return self.__wrap__('__ror__', True, '{}|{}'.format(*map(repr, (other, self))), other)

    def __rxor__(self, other):
        return self.__wrap__('__rxor__', True, '{}^{}'.format(*map(repr, (other, self))), other)

    def __rlshift__(self, other):
        return self.__wrap__('__rlshift__', True, '{} << {}'.format(*map(repr, (other, self))), other)

    def __rrshift__(self, other):
        return self.__wrap__('__rrshift__', True, '{} >> {}'.format(*map(repr, (other, self))), other)

    # operation insert
    def __iadd__(self, other):
        return self.__wrap__('__iadd__', True, '{} += {}'.format(*map(repr, (self, other))), other)

    def __isub__(self, other):
        return self.__wrap__('__isub__', True, '{} -= {}'.format(*map(repr, (self, other))), other)

    def __imul__(self, other):
        return self.__wrap__('__imul__', True, '{} *= {}'.format(*map(repr, (self, other))), other)

    def __ipow__(self, other):
        return self.__wrap__('__ipow__', True, '{} **= {}'.format(*map(repr, (self, other))), other)

    def __imatmul__(self, other):
        return self.__wrap__('__imatmul__', True, '{} @= {}'.format(*map(repr, (self, other))), other)

    def __itruediv__(self, other):
        return self.__wrap__('__itruediv__', True, '{} /= {}'.format(*map(repr, (self, other))), other)

    def __ifloordiv__(self, other):
        return self.__wrap__('__ifloordiv__', True, '{} //= {}'.format(*map(repr, (self, other))), other)

    def __imod__(self, other):
        return self.__wrap__('__imod__', True, '{} %= {}'.format(*map(repr, (self, other))), other)

    # binary operation
    def __iand__(self, other):
        return self.__wrap__('__iand__', True, '{} &= {}'.format(*map(repr, (self, other))), other)

    def __ior__(self, other):
        return self.__wrap__('__ior__', True, '{} |= {}'.format(*map(repr, (self, other))), other)

    def __ixor__(self, other):
        return self.__wrap__('__ixor__', True, '{} ^= {}'.format(*map(repr, (self, other))), other)

    def __ilshift__(self, other):
        return self.__wrap__('__ilshift__', True, '{} <<= {}'.format(*map(repr, (self, other))), other)

    def __irshift__(self, other):
        return self.__wrap__('__irshift__', True, '{} >>= {}'.format(*map(repr, (self, other))), other)

    # unary
    def __neg__(self):
        return self.__wrap__('__neg__', False, '-{}'.format(repr(self)))

    def __pos__(self):
        return self.__wrap__('__pos__', False, '+{}'.format(repr(self)))

    def __invert__(self):
        return self.__wrap__('__invert__', False, '~{}'.format(repr(self)))

    # accessing
    def __getattr__(self, item):
        return self.__wrap__('__getattr__', False, '{}.{}'.format(repr(self), item), item)

    def __getitem__(self, item):
        return self.__wrap__('__getitem__', False, '{}[{}]'.format(repr(self), item), item)


class XObject(XAbstract):
    def __init__(self, func, name, repr_):
        self.__func = func
        self.__name = name
        self.__repr = repr_

    def __repr__(self):
        return '({})'.format(self.__repr)

    def __run__(self, x):
        return self.__func(x)

    def __wrap__(self, name, operation, repr_, *args, **kwargs):
        def _run(x):
            result = self.__run__(x)
            return getattr(type(x), name)(result, *[
                XAbstract.process_x(value, x)
                for value in args
            ], **{
                key: XAbstract.process_x(value, x)
                for key, value in kwargs.items()
            })
        return (XOperation if operation else XObject)(_run, name, repr_)


class XClass(XAbstract):
    def __repr__(self):
        return 'X'

    def __run__(self, x):
        return x

    def __wrap__(self, name, operation, repr_, *args, **kwargs):
        def _run(x):
            return getattr(type(x), name)(x, *(
                XAbstract.process_x(value, x)
                for value in args
            ), **{
                key: XAbstract.process_x(value, x)
                for key, value in kwargs.items()
            })
        return (XOperation if operation else XObject)(_run, name, repr_)


class XOperation(XObject):
    def __call__(self, x):
        return self.__run__(x)


class XPartial:
    def __init__(self, callable_: Callable, *args, **kwargs):
        self.callable = callable_
        self.args = XAccess(args)
        self.kwargs = XAccess(kwargs)

    def __call__(self, x):
        return self.callable(*self.args(x), **self.kwargs(x))

    def __repr__(self):
        return '{callable}(*{args}, **{kwargs})'.format(callable=self.callable,
                                                        args=self.args,
                                                        kwargs=self.kwargs)


class XAccess:
    def __init__(self, arg: Union[XAbstract, Dict, Iterable, Any]):
        self.arg = arg

    def __call__(self, x):
        if isinstance(self.arg, XAbstract):
            return type(self.arg).__run__(self.arg, x)
        if isinstance(self.arg, Dict):
            return type(self.arg)((key, XAccess(inner_arg)(x)) for key, inner_arg in self.arg.items())
        if isinstance(self.arg, Iterable):
            return type(self.arg)(XAccess(inner_arg)(x) for inner_arg in self.arg)
        if isinstance(self.arg, XPartial):
            return self.arg(x)
        return self.arg

    def __repr__(self):
        return 'XAccess x: {}'.format(repr(self.arg).replace('X', 'x'))


class FClass:
    def __getitem__(self, item):
        return XAccess(item)


X = XClass()
F = FClass()
Partial = XPartial
