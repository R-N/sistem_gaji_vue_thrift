from .download import DownloadModel
from .upload import UploadModel
from .email import EmailModel

from .manager import models

models['download'] = DownloadModel()
models['upload'] = UploadModel()
models['email'] = EmailModel()