from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import reconstructor

def pk_periode():
    return Column(Date, ForeignKey('periode_gaji.periode'), primary_key=True)

def has_periode(cls):
    return (isinstance(cls, bool) and cls) or hasattr(cls, "periode")


def has_enabled(cls):
    return (isinstance(cls, bool) and cls) or hasattr(cls, "enabled")


def pop_periode(cls, arr):
    if has_periode(cls):
        return arr
    return arr[1:]


def insert_periode(cls, arr):
    if has_periode(cls):
        return [cls.periode] + arr
    return arr


class MxPkPeriode:
    @declared_attr
    def periode(cls):
        return pk_periode()

    def periode_init(self, periode):
        self.periode = periode

    def periode_repr(self):
        return "periode=%r, %s" % (self.periode, self.mx_repr())


class MxAiId:
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, autoincrement=has_periode(cls))


class MxEnabled:
    @declared_attr
    def enabled(cls):
        return Column(Boolean, nullable=False, default=True)

    def enabled_init(self, enabled):
        self.enabled = enabled

    def enabled_repr(self):
        return "%s, enabled=%r" % (self.mx_repr(), self.enabled)


class MxRepr:
    @declared_attr
    def repr_repr(cls):
        repr_str = cls.__name__ + "(%s)"
        if has_periode(cls):
            def __repr__(self):
                return repr_str % (self.periode_repr(),)
            return __repr__
        elif has_enabled(cls):
            def __repr__(self):
                return repr_str % (self.enabled_repr(),)
            return __repr__
        else:
            def __repr__(self):
                return repr_str % (self.mx_repr(),)
            return __repr__

    @declared_attr
    def __repr__(cls):
        return cls.repr_repr


class MxCommited(MxRepr, MxPkPeriode):
    def __init__(
        self,
        periode,
        *args,
        **kwargs
    ):
        self.mx_init(
            *args,
            **kwargs
        )
        self.periode_init(periode)

    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()


class MxStaging(MxRepr, MxEnabled):
    def __init__(
        self,
        *args,
        enabled,
        **kwargs
    ):
        self.mx_init(
            *args,
            **kwargs
        )
        self.enabled_init(enabled)

    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()
