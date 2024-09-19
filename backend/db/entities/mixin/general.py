from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import reconstructor
from sqlalchemy.ext.hybrid import hybrid_property


def pk_periode():
    return Column("periode", Date, ForeignKey('periode_gaji.periode', ondelete="RESTRICT"), primary_key=True)


def has_periode(cls):
    return (isinstance(cls, bool) and cls) or hasattr(cls, "periode")


def has_enabled(cls):
    return (isinstance(cls, bool) and cls) or hasattr(cls, "enabled")


def eager_load_staging_parent(cls):
    return "select" if has_periode(cls) else "selectin"


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

    '''
    def periode_init(self, periode):
        self.periode = periode
    '''

    def periode_repr(self):
        return "periode=%r, %s" % (self.periode, self.mx_repr())


class MxAiId:
    @declared_attr
    def id(cls):
        return Column("id", Integer, primary_key=True, autoincrement=not has_periode(cls))

    def id_init(self, id=None):
        if id is not None:
            self.id = id


class MxEnabled:
    @declared_attr
    def enabled(cls):
        return Column("enabled", Boolean, nullable=False, default=True)
    '''
    def enabled_init(self, enabled):
        self.enabled = enabled
    '''

    def enabled_repr(self):
        return "%s, enabled=%r" % (self.mx_repr(), self.enabled)

    @declared_attr
    def real_enabled(cls):
        @hybrid_property
        def real_enabled(self):
            return self.enabled

        @real_enabled.expression
        def real_enabled(cls):
            return cls.enabled

        return real_enabled


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


class MxReconstruct:
    @reconstructor
    def reconstruct(self):
        self.mx_reconstruct()


class MxEntity(MxReconstruct, MxRepr):
    pass


class MxCommited(MxEntity, MxPkPeriode):
    '''
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
    '''
    pass


class MxAlwaysEnabled:
    @declared_attr
    def enabled(cls):
        @hybrid_property
        def enabled(self):
            return True

        @enabled.expression
        def enabled(cls):
            return True

        return enabled

    @declared_attr
    def real_enabled(cls):
        @hybrid_property
        def real_enabled(self):
            return True

        @real_enabled.expression
        def real_enabled(cls):
            return True

        return real_enabled

    @declared_attr
    def set_enabled(cls):
        def set_enabled(self, enabled):
            raise Exception("Always enabled")
        return set_enabled


class MxStagingLite(MxAlwaysEnabled, MxEntity):
    pass


class MxStaging(MxEnabled, MxStagingLite):
    '''
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
    '''
    pass
