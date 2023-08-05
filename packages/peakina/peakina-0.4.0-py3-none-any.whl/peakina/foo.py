class A:
    _registry = {}
    _registry2 = {}

    @classmethod
    def __init_subclass__(cls, *, schemes):
        print('cls', cls, schemes)
        super().__init_subclass__()
        for scheme in schemes:
            cls._registry[scheme] = cls


def register(schemes):
    def _register(cls):
        for s in schemes:
            cls._registry2[s] = cls
        return cls

    return _register


@register(['foo'])
class B(A, schemes=['foo']):
    pass


@register(['bar'])
class C(A, schemes=['bar']):
    pass
