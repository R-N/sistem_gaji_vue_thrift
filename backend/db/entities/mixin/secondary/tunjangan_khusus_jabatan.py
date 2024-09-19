from sqlalchemy import Column, Integer, ForeignKeyConstraint, Table, Date, ForeignKey
from ..general import pop_periode, has_periode

def ScTunjanganKhususJabatan(metadata, cls):
    meta = [
        'tunjangan_khusus_jabatan',
        metadata
    ]

    cols = [
        Column('tunjangan_khusus_id', Integer, nullable=False, primary_key=True),
        Column('jabatan_id', Integer, nullable=False, primary_key=True)
    ]

    if has_periode(cls):
        cols = [Column('periode', Date, ForeignKey('periode_gaji.periode'), primary_key=True)] + cols

    fks = [
        ForeignKeyConstraint(
            pop_periode(cls, ["periode", "tunjangan_khusus_id"]),
            pop_periode(cls, ["tunjangan_khusus.periode", "tunjangan_khusus.id"]),
            deferrable=True,
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            pop_periode(cls, ["periode", "jabatan_id"]),
            pop_periode(cls, ["jabatan.periode", "jabatan.id"]),
            deferrable=True,
            ondelete="RESTRICT",
        )
    ]

    return Table(*meta, *cols, *fks, extend_existing=True)

