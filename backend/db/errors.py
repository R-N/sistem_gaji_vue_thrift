from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes as pg_errorcodes
import re

class MyIntegrityError(IntegrityError):
    def __init__(self, src):
        super(MyIntegrityError, self).__init__(
            src.statement,
            src.params,
            src.orig,
            hide_parameters=src.hide_parameters,
            connection_invalidated=src.connection_invalidated,
            ismulti=src.ismulti
        )

    @classmethod
    def check(cls, src):
        return src.orig.pgcode == cls.CODE

class UniqueError(MyIntegrityError):
    CODE = pg_errorcodes.UNIQUE_VIOLATION
    REGEX = re.compile(
        r'duplicate.*violat.*unique.*\"(.*)\".*Key *\((.*)\)\=\((.*)\)', 
        re.IGNORECASE | re.MULTILINE | re.DOTALL
    )

    def __init__(self, src):
        super(UniqueError, self).__init__(src)
        error = src.orig.pgerror
        self.match = UniqueError.REGEX.search(error)
        self.constraint = self.match.group(1)
        self.column = self.match.group(2)
        self.value = self.match.group(3)

# TODO
class ForeignKeyError(MyIntegrityError):
    CODE = pg_errorcodes.FOREIGN_KEY_VIOLATION

    def __init__(self, src):
        super(ForeignKeyError, self).__init__(src)


class NotNullError(MyIntegrityError):
    CODE = pg_errorcodes.NOT_NULL_VIOLATION
    REGEX = re.compile(
        r'null.*\"(.*)\".*violat.*not\-null',
        re.IGNORECASE | re.MULTILINE | re.DOTALL
    )

    def __init__(self, src):
        super(NotNullError, self).__init__(src)
        error = src.orig.pgerror
        self.match = NotNullError.REGEX.search(error)
        self.constraint = "not-null"
        self.column = self.match.group(1)
        self.value = None

# TODO
class RestrictError(MyIntegrityError):
    CODE = pg_errorcodes.RESTRICT_VIOLATION

    def __init__(self, src):
        super(RestrictError, self).__init__(src)

def parse_db_error(src):
    if UniqueError.check(src):
        return UniqueError(src)
    if ForeignKeyError.check(src):
        return ForeignKeyError(src)
    if NotNullError.check(src):
        return NotNullError(src)
    if RestrictError.check(src):
        return RestrictError(src)
    return None