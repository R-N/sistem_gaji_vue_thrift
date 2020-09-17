from .auth import AuthModel
from .user import UserModel
from .backup import BackupModel
from .download import DownloadModel
from .upload import UploadModel
from .email import EmailModel
from .manager import set_model, get_model

set_model('auth', AuthModel())
set_model('user', UserModel())
set_model('backup', BackupModel())
set_model('upload', UploadModel())
set_model('download', DownloadModel())
set_model('email', EmailModel())