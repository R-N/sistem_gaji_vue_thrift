from .auth import AuthModel
from .user import UserModel
from .backup import BackupModel

models = {}

def get_model(name):
	return models[name]

def set_model(name, model):
	global models
	models[name] = model

set_model('auth', AuthModel())
set_model('user', UserModel())
set_model('backup', BackupModel())