from .auth import AuthModel
from .user import UserModel
from .backup import BackupModel
from .email import EmailModel
from .perusahaan import PerusahaanModel

from .manager import models, basic_models

models['auth'] = AuthModel()
models['user'] = UserModel()
models['backup'] = BackupModel()
models['email'] = EmailModel()
models['perusahaan'] = PerusahaanModel()