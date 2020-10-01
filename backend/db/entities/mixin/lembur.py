from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from .general import pop_periode
from .lembur_base import MxLemburBase


class MxLembur(MxLemburBase):

    @declared_attr
    def makan(cls):
        return Column(Boolean, nullable=False, default=False)

    @declared_attr
    def transport(cls):
        return Column(Boolean, nullable=False, default=False)

    '''
    def mx_init(
        self,
        *args,
        makan=False,
        transport=False,
        **kwargs
    ):
        MxLemburBase.mx_init(self, *args, **kwargs)
        self.makan = makan
        self.transport = transport
    '''

    def mx_reconstruct(self):
        MxLemburBase.mx_reconstruct(self)

    def mx_repr(self):
        return "%s, makan=%r, transport=%r" % (MxLemburBase.mx_repr(self), self.makan, self.transport)

    def mx_init_repr(self):
        ret = MxLemburBase.mx_init_repr(self)
        ret.update({
            'makan': self.makan,
            'transport': self.transport
        })
        return ret
