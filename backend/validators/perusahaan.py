from rpc.gen.data.perusahaan.errors.ttypes import TPerusahaanError, TPerusahaanErrorCode
import rpc.gen.data.perusahaan.errors.constants as perusahaan_constants
from db.errors import UniqueError

def validate_nama(nama):
    if not nama:
        raise TPerusahaanError(TPerusahaanErrorCode.NAMA_EMPTY)
    if len(nama) > perusahaan_constants.NAMA_LEN_MAX:
        raise TPerusahaanError(TPerusahaanErrorCode.NAMA_TOO_LONG)


def parse_error(parsed):
    if isinstance(parsed, UniqueError):
        if parsed.column == "email":
            raise TPerusahaanError(TPerusahaanErrorCode.EMAIL_ALREADY_EXISTS)